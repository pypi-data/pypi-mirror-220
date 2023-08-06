# Library of SPAM image correlation functions.
# Copyright (C) 2020 SPAM Contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import time  # for debug

import numpy
import spam.DIC
import spam.label  # for label tet
import tifffile

# 2017-05-29 ER and EA
# This is spam's C++ DIC toolkit, but since we're in the tools/ directory we can import it directly
from spam.DIC.DICToolkit import (
    computeDICglobalMatrix,
    computeDICglobalVector,
    computeGradientPerTet,
)


def _errorCalc(im1, im2, im2ref, meshPaddingSlice):
    errorInitial = numpy.sqrt(numpy.square(im2ref[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
    errorCurrent = numpy.sqrt(numpy.square(im2[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
    return errorCurrent / errorInitial


def _makeRegularisationMatrix(regularisation, points, connectivity, Mc):

    # 1. check minimal number of parameters
    # 1.1: check mesh type
    try:
        MESH = regularisation["MESH"]
        MESH_TYPE = MESH.get("type", "cuboid")
    except KeyError as e:
        raise KeyError(f"[regularisation] Missing parameter: {e}")

    # 1.2: check mandatory BULK
    try:
        BULK = regularisation["BULK"]
        BULK_YOUNG = BULK["young"]
        BULK_POISSON = BULK["poisson"]
        BULK_KSI = BULK["ksi"]
    except KeyError as e:
        raise KeyError(f"[regularisation] Missing parameter in BULK: {e}")
    # 1.2 check cast not mandatory BULK
    BULK_FEW = BULK.get("few_times", 3.0)  # we still need to figure out what it means
    print(f"[regularisation] [neumann] young = {BULK_YOUNG}")
    print(f"[regularisation] [neumann] poisson = {BULK_POISSON}")
    print(f"[regularisation] [neumann] ksi = {BULK_KSI}")
    print(f"[regularisation] [neumann] few = {BULK_FEW}")

    # 1.3: check dirichlet
    DIRICHLET = regularisation.get("DIRICHLET")
    try:
        if DIRICHLET:
            DIRICHLET_SURFACES = [(k, v) for k, v in DIRICHLET["ksi"].items() if isinstance(v, int)]
        else:
            DIRICHLET_SURFACES = []
    except KeyError as e:
        raise KeyError(f"Missing parameter in DIRICHLET: {e}")

    print(f'[regularisation] [dirichlet] Surface regularisation activated: {"yes" if DIRICHLET else "no"}')
    if DIRICHLET:
        for k, v in DIRICHLET_SURFACES:
            # k is where, v is ksi
            print(f"[regularisation] [dirichlet]\t{k}: {v}")

    # 2. compute complete connectivity matrix
    K = spam.mesh.globalStiffnessMatrix(points, connectivity, BULK_YOUNG, BULK_POISSON)

    # 3. compute projection matrices
    # note: for cylinders we can't deduce the surface from the mesh
    # so it will need to be a user input in `regularisation`
    # diagonal matrix with 1 only on surface dof
    DS = numpy.zeros_like(K)
    # diagonal matrix with 1 only on surface with dirichlet dof for each
    # surface
    n_dirichlet = len(DIRICHLET_SURFACES)
    print(f"[regularisation] [dirichlet] number of surfaces -> {n_dirichlet}")
    DSd = []
    DSd_A = []
    DSd_B = []
    DSd_nn = []
    DSd_en = []
    for si in range(n_dirichlet):
        DSd.append(numpy.zeros_like(K))
        DSd_A.append(numpy.zeros_like(K))  # A matrix (to be inverted)
        DSd_B.append(numpy.zeros_like(K))  # B matrix (A.B = I)
        DSd_nn.append([])  # list of all node numbers on dirichlet surfaces
        DSd_en.append([])  # list of all equations on dirichlet surfaces

    # diagonal matrix with 1 only on surface with neuman dof
    DSn = numpy.zeros_like(K)
    if MESH_TYPE == "cuboid":
        # we assume it's a cuboid to define the surfaces
        # 1 x 6 array with [min_z, min_y, min_x, max_z, max_y, max_x]
        maxCoord = numpy.amax(points, axis=0).astype("<u2")
        minCoord = numpy.amin(points, axis=0).astype("<u2")
        surfaces_positions = list(minCoord) + list(maxCoord)
        print(f"[regularisation] [dirichlet] compute surfaces based on min/max mesh coordinates: {surfaces_positions}")

        # a list of [direction, positions fo reach surface]
        def _dirpos(key, surfaces_positions):
            """Simple parsing function that takes surface keys
            z_start, z_end, y_start, y_end, x_start, x_end
            and convert it to (direction, position) based on surfaces_positions

            surface_positions = [min_z, min_y, min_x, max_z, max_y, max_x]
            """
            # split key
            dir_str, pos_str = key.split("_")

            # convert direction into integer
            _str2int = {"z": 0, "y": 1, "x": 2}
            direction = _str2int[dir_str]

            # convert position into coordinate
            _str2int = {"s": 0, "e": 1}
            position = surfaces_positions[3 * _str2int[pos_str[0]] + direction]

            print(f"[regularisation] [dirichlet] BC {key} -> {direction}, {position}")

            return direction, position  # needs to be a tuple for later lookup

        bcd_lookup = [_dirpos(key, surfaces_positions) for key, _ in DIRICHLET_SURFACES]
        if DIRICHLET:
            print(f"[regularisation] [dirichlet] BC bcd_lookup = {bcd_lookup}")

        # loop over the points
        # PUT SOME NUMBA HERE
        for A, point in enumerate(points):
            # print(f"[regularisation] point {A} {point} ({A/points.shape[0]*100:.2f}%)")
            # loop over the surfaces to find if current point belongs to it
            # A: global point number
            # point: [z, y, x] coordinate

            # get all the dofs for surfaces: DS
            for direction, position in enumerate(surfaces_positions):
                # since surfaces_positions =
                #         [min_z, min_y, min_x, max_z, max_y, max_x]
                # position is alternatively min_z, min_y, ...
                # with mod 3 direction is 0, 1, 2, 0, 1, 2
                direction = direction % 3  # due to concatenation of min/max
                # check point position
                if abs(point[direction] - position) < 0.00001:
                    # print(f"[regularisation] Point number {A}: {point} in surface N{direction} = {position}")
                    # loop over the 3 dofs / deduce global equation number
                    for i in range(3):
                        # P: global equation number
                        P = 3 * A + i
                        DS[P, P] = 1

                        # check if also dirichlet
                        if DIRICHLET:
                            try:
                                # WARNING: position is float so we need to be
                                # more careful about the comparison we make here
                                # as one comes from user input and the other from
                                # node coordinates
                                # maybe use numpy.isclose
                                si = bcd_lookup.index((direction, position))
                                DSd[si][P, P] = 1
                                DSd_nn[si].append(A)
                                DSd_en[si].append(P)
                                # print(f'Dirichlet Surface {si} point {A} {P}')
                            except ValueError:
                                DSn[P, P] = 1
                        else:
                            DSn[P, P] = 1

                    # with the break the point will be assigned to the
                    # first surface of the loop (ie we could miss some
                    # dirichlet bc if neuman comes first).
                    # And since we don't have the control over the ordering
                    # of the surface it's not a really good thing
                    # break

        # WARNING/TODO: without the break above, points on
        # edges can be assigne to multiple surfaces
        # for edges between two surfaces of the same kind
        # it's okay but edges between neuman and dirchlet
        # pose a problem.
        # Might be good to clean the neumann matrix where there overlap to give
        # priority to dirichlet

    elif MESH_TYPE == "cylinder":
        # later check the good parameters needed (center/radius/orientation)
        raise NotImplementedError("Cylindrical meshes are not implement yet")
    else:
        raise KeyError(f"Unknown mesh type {MESH_TYPE}")

    # loop over all tetraedra to build up triangle meshes of dirichlet
    # convert node numbers into sets
    dirichlet_connectivity_all = []
    dirichlet_points_all = []
    for si in range(n_dirichlet):
        DSd_nn[si] = set(DSd_nn[si])
        dirichlet_connectivity_all.append([])
        dirichlet_points_all.append([])

    # loop over dirichlet matrix
    for si, surface_node_numbers in enumerate(DSd_nn):
        for tetra_connectivity in connectivity:
            tri_con = list(surface_node_numbers.intersection(tetra_connectivity))
            tri_nodes = [list(points[i]) for i in tri_con]
            if len(tri_con) != 3:
                # the element doesn't have a triangle a this surface
                continue

            # get 4th point of the tetrahedron to compute 3D shape functions
            point_4_n = list(set(tri_con).symmetric_difference(set(tetra_connectivity)))[0]
            _, tri_coefficients = spam.mesh.shapeFunctions(tri_nodes + [list(points[point_4_n])])
            # we've got a triangle on the surface!!!
            # dirichlet_direction = regularisation["bc_dirichlet"][si][2]
            dirichlet_connectivity_all[si].append(list(tri_con))
            dirichlet_points_all[si].append(tri_nodes)

            # assemble the dirichlet connectivity matrix
            a = numpy.array(tri_coefficients[:3, 0])
            bcd = numpy.array(tri_coefficients[:3, 1:])
            B = numpy.array(tri_nodes).T

            def phi(i, L):
                return a[i] + numpy.matmul(bcd[i], numpy.matmul(B, L.T))

            def dphi(i):
                return bcd[i]

            # gauss points
            L_gp = numpy.array([[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])

            # STEP 3: compute the area
            area = 0.5 * numpy.linalg.norm(
                numpy.cross(
                    numpy.subtract(tri_nodes[1], tri_nodes[0]),
                    numpy.subtract(tri_nodes[2], tri_nodes[0]),
                )
            )

            # STEP 3: compute inner products of the shape functions
            for i in range(3):
                for j in range(3):
                    inner = 0.0
                    for L in L_gp:
                        # print(inner, i, j, L, phi(i, L), phi(j, L))
                        inner += phi(i, L) * phi(j, L)
                    inner *= area / 3.0  # the 1/3. comes from the weight
                    dinner = area * numpy.inner(dphi(i), dphi(j))
                    for dirichlet_direction in range(3):
                        P = 3 * tri_con[i] + dirichlet_direction
                        Q = 3 * tri_con[j] + dirichlet_direction
                        DSd_A[si][P, Q] += inner
                        DSd_B[si][P, Q] += dinner

    for si in range(n_dirichlet):
        # invert matrix A
        # 1. extract submatrix A from full size DSd_A and invert
        sub_A = DSd_A[si][:, DSd_en[si]]
        sub_A = numpy.linalg.inv(sub_A[DSd_en[si], :])
        # 2. push back inverted submatrix into full size DSd_A
        for i, P in enumerate(DSd_en[si]):
            for j, Q in enumerate(DSd_en[si]):
                DSd_A[si][P, Q] = sub_A[i, j]

    # DEBUG
    # for si, _ in enumerate(dirichlet_connectivity_all):
    #     a = numpy.array(dirichlet_connectivity_all[si])
    #     meshio.write_points_cells(
    #         f'dirichlet_{si}.vtk',
    #         points,
    #         {'triangle': a},
    #         file_format='vtk',
    #         binary=False
    #     )

    # diagonal matrix with 1 only on bulks dof
    DB = numpy.eye(K.shape[0]) - DS

    # 4.1 build bulk connectivity matrix
    Km = numpy.matmul(DB + DSn, K)
    # 4.2 build dirichlet connectivity matrices
    Ks = [numpy.matmul(DSd_i, K) for DSd_i in DSd]

    # 5. normalisation of each functionals
    # 5.1: build v(x) = sin(2pi k.x)
    # lookup for largest dimension to build k
    lengths = [0, 0, 0]
    for i in range(3):
        lengths[i] = surfaces_positions[i + 3] - surfaces_positions[i]
    largest_direction = numpy.argmax(lengths)
    largest_size = numpy.max(lengths)
    k = [0, 0, 0]
    k_mag = BULK_FEW / float(largest_size)
    k[largest_direction] = k_mag
    # print(f"[regularisation] k = {k} |k| = {numpy.linalg.norm(k)} 1/|k| = {1.0 / numpy.linalg.norm(k)}")

    # build pure shear field for normalisation
    v = []
    for point in points:
        vector = [0, 0, 0]
        norm = numpy.sin(2 * numpy.pi * numpy.dot(k, point))
        vector[(largest_direction + 1) % 3] = numpy.sqrt(0.5) * norm
        vector[(largest_direction + 2) % 3] = numpy.sqrt(0.5) * norm
        # vector[(largest_direction + 1) % 3] = norm
        v.append(vector)
        # print(point, k, numpy.dot(k, point), norm, vector)

    # debug build vtk with v(x) on current mesh
    v = numpy.array(v)
    spam.helpers.writeUnstructuredVTK(
        points,
        connectivity,
        elementType="tetra",
        pointData={"v": v},
        cellData={},
        fileName="debug-regularisation-v.vtk",
    )

    # 5.2 compute normalized energies
    v = numpy.ravel(v)
    Ec = numpy.matmul(v.T, numpy.matmul(Mc, v))
    Em = numpy.matmul(v.T, numpy.matmul(Km.T, numpy.matmul(Km, v)))
    Es = [
        numpy.matmul(
            v.T,
            numpy.matmul(
                Ks[i].T,
                numpy.matmul(DSd_A[i], numpy.matmul(DSd_B[i], numpy.matmul(Ks[i], v))),
            ),
        )
        for i in range(n_dirichlet)
    ]

    Es_string = " ".join([f"{_:.0f}" for _ in Es])
    print(f"[regularisation] Ec = {Ec:.0f}, Em = {Em:.0f}, Es = {Es_string}")

    # 5.3 compute functional weights
    # 5.3.1 DVC weight
    omega_c = 1.0

    # 5.3.2 Neumann weight
    ksi = BULK_KSI if BULK_KSI else 1.0 / k_mag
    print(f"[regularisation] [neumann] ksi = {ksi}")
    omega_m = (ksi * numpy.linalg.norm(k)) ** 4

    # 5.3.3 Dirichlet weight
    omega_s = []
    for _, ksi in DIRICHLET_SURFACES:
        if ksi == 0:  # compute value based on k_mag
            ksi = 1.0 / k_mag
            print(f"[regularisation] [dirichlet] use 1/k_mag for ksi for surface {_}: {ksi}")
        omega_s.append((ksi * numpy.linalg.norm(k)) ** 4)

    # 5.3.4 Total weigth for normalisation
    omega_t = omega_c + omega_m + sum(omega_s)

    print(f"[regularisation] omega_t   = {omega_t:.2f}")
    print(f"[regularisation] omega_c   = {omega_c:.2f} ({100 * (omega_c / omega_t):.2f}%)")
    print(f"[regularisation] omega_m   = {omega_m:.2f} ({100 * (omega_m / omega_t):.2f}%)")
    for i, omega in enumerate(omega_s):
        print(f"[regularisation] omega_s_{i} = {omega} ({100 * (omega / omega_t):.2f}%)")

    # weight_m = omega_m * Ec / Em
    # weight_s = [omega_s[i] * Ec / Es[i] for i in range(n_dirichlet)]
    # print(f"[regularisation] weight_m = {weight_m}, weight_s = {weight_s}")

    # 5.4 compute Mreg
    Mreg = numpy.zeros_like(K)
    Mreg = Ec * omega_m * numpy.matmul(Km.T, Km) / Em
    for si in range(n_dirichlet):
        Mreg += omega_s[si] * Ec * numpy.matmul(Ks[si].T, numpy.matmul(DSd_A[si], numpy.matmul(DSd_B[si], Ks[si]))) / Es[si]

    # from matplotlib import pyplot as plt
    # # plt.imshow(numpy.log(Mreg))
    # plt.imshow(numpy.log(Mreg))
    # plt.show()
    # plt.imshow(numpy.log(Mc))
    # plt.show()

    # def phi_t(u):
    #     omega_t = omega_c + omega_m
    #     phi_c = omega_c * numpy.matmul(u.T, numpy.matmul(Mc, u)) / Ec
    #     phi_c += omega_m * numpy.matmul(u.T, numpy.matmul(Km.T, numpy.matmul(Km, u))) / Em
    #     phi_c /= omega_t
    #     return phi_c
    # return

    return Mreg


def globalCorrelation(
    im1,
    im2,
    points,
    connectivity,
    regularisation={},
    initialDisplacements=None,
    convergenceCriterion=0.01,
    maxIterations=20,
    medianFilterEachIteration=False,
    debugFiles=False,
    prefix="globalCorrelation",
    nThreads=None,
):
    """
    Global DVC (works only with 3D images).

    Parameters
    ----------
        im1 : 3D numpy array
            Reference image in which the mesh is defined

        im2 : 3D numpy array
            Deformed image, should be same size as im1

        points :  M x 3 numpy array
            M nodal coordinates in reference configuration

        connectivity : N x 4 numpy array
            connectivityhedral connectivity generated by spam.mesh.triangulate() for example

        regularisation : dict (optional)
            regularisation parameters

            .. code-block:: python

                # ksi is a normalisation parameter to control the weight
                # of each functionals (DVC, bulk and surface).
                # If set to 0 it will be automatically computed.

                # Example for a cuboid mesh
                {
                    # Information about the mesh
                    "MESH": {"type": "cuboid"},  # mandatory
                    # Information about the elastic regularisation
                    # (Bulk + Neumann boundary conditions)
                    "BULK": {
                        "young": 10,  # mandatory (Young modulus)
                        "poisson": 0.25,  # mandatory (Poisson ratio)
                        "ksi": 30,  # mandatory
                        "few_times": 3,  # optionnal (whatever...)
                    },
                    # Information about the surface regularisation
                    # (Dirichlet boundary conditions)
                    # Each surface of the cuboid is labelled by the keywords
                    # z_start: z == 0, z_end, y_start, y_end, x_start and x_end)
                    # If a keyword is ommited the surface is not regularised.
                    "DIRICHLET": {
                        "ksi": {  # mandatory
                            "z_start": 0,  # automatically computed
                            "z_end": 30,  # ksi normalisation is 30
                        }
                    },
                }

        initialDisplacements : M x 3 numpy array of floats (optional)
            Initial guess for nodal displacements, must be coherent with input mesh
            Default = None

        convergenceCriterion : float
            Convergence criterion for change in displacements in px
            Default = 0.01

        maxIterations : int
            Number of iterations to stop after if convergence has not been reached
            Default = 20

        debugFiles : bool
            Write temporary results to file for debugging?
            Default = 'globalCorrelation'

        prefix : string
            Output file prefix for debugFiles
            Default = None

    Returns
    -------
        displacements : N x 3 numpy array of floats
            (converged?) Nodal displacements

    Example
    -------
        >>> import spam.DIC
        >>> spam.DIC.globalCorrelation(
            imRef,
            imDef
        )
    """
    import multiprocessing

    import spam.helpers
    import spam.mesh

    # Global number of processes
    nThreads = multiprocessing.cpu_count() if nThreads is None else nThreads
    print(f"[globalCorrelation] C++ parallelisation on {nThreads} threads")

    print(f"[globalCorrelation] Convergence criterion = {convergenceCriterion}")
    print(f"[globalCorrelation] Max iterations = {maxIterations}")
    print("[globalCorrelation] Converting im1 to 32-bit float")
    im1 = im1.astype("<f4")

    points = points.astype("<f8")
    connectivity = connectivity.astype("<u4")

    maxCoord = numpy.amax(points, axis=0).astype("<u2")
    minCoord = numpy.amin(points, axis=0).astype("<u2")
    print(f"[globalCorrelation] Mesh box: min = {minCoord} max = {maxCoord}")

    meshPaddingSlice = (
        slice(minCoord[0], maxCoord[0]),
        slice(minCoord[1], maxCoord[1]),
        slice(minCoord[2], maxCoord[2]),
    )

    displacements = numpy.zeros((points.shape[0], 3), dtype="<f8")

    print(f"[globalCorrelation] Points: {points.shape}")
    print(f"[globalCorrelation] Displacements: {displacements.shape}")
    print(f"[globalCorrelation] Cells: {connectivity.shape}")
    print(f"[globalCorrelation] Padding: {meshPaddingSlice}")

    ###############################################################
    # Step 2-1 Apply deformation and interpolate pixels
    ###############################################################

    print("[globalCorrelation] Allocating 3D data (deformed image)")
    if initialDisplacements is None:
        im1Def = im1.copy()
        imTetLabel = spam.label.labelTetrahedra(im1.shape, points, connectivity, nThreads=nThreads)
    else:
        print("[globalCorrelation] Applying initial deformation to image")
        displacements = initialDisplacements.copy()
        tic = time.perf_counter()
        imTetLabel = spam.label.labelTetrahedra(im1.shape, points + displacements, connectivity, nThreads=nThreads)
        print(f"[globalCorrelation] Running labelTetrahedra: {time.perf_counter()-tic:.3f} seconds.")

        im1Def = spam.DIC.applyMeshTransformation(
            im1,
            points,
            connectivity,
            displacements,
            imTetLabel=imTetLabel,
            nThreads=nThreads,
        )
        if debugFiles:
            print("[globalCorrelation] Saving initial images")
            for name, image in [
                [f"{prefix}-def-init.tif", im1Def],
                [f"{prefix}-imTetLabel-init.tif", imTetLabel],
            ]:
                print(f"[globalCorrelation]\t{name}: {image.shape}")
                tifffile.imwrite(name, image)

    # print("[globalCorrelation] Correlating (MF)!")
    print("[globalCorrelation] Calculating gradient of IM TWO...")
    im2Grad = numpy.array(numpy.gradient(im2), dtype="<f4")

    print("[globalCorrelation] Computing global matrix")
    # This generates the globalMatrix (big Mc matrix) with imGrad as input
    Mc = numpy.zeros((3 * points.shape[0], 3 * points.shape[0]), dtype="<f8")

    if debugFiles:
        print("[globalCorrelation] Computing debug files fields")
        gradientPerTet = numpy.zeros((connectivity.shape[0], 3), dtype="<f8")
        IDPerTet = numpy.array([_ for _ in range(connectivity.shape[0])])

        computeGradientPerTet(
            imTetLabel.astype("<u4"),
            im2Grad.astype("<f4"),
            connectivity.astype("<u4"),
            (points + displacements).astype("<f8"),
            gradientPerTet,
        )

        spam.helpers.writeUnstructuredVTK(
            (points + displacements),
            connectivity,
            cellData={"meanGradient": gradientPerTet, "id": IDPerTet},
            fileName=f"{prefix}-gradient.vtk",
        )
        del gradientPerTet

    computeDICglobalMatrix(
        imTetLabel.astype("<u4"),
        im2Grad.astype("<f4"),
        connectivity.astype("<u4"),
        (points + displacements).astype("<f8"),
        Mc,
    )

    ###############################################################
    # Setup left hand vector
    ###############################################################
    if len(regularisation):
        print("[globalCorrelation] Entering regularisation")
        Mreg = _makeRegularisationMatrix(regularisation, points, connectivity, Mc)
        left_hand_inverse = numpy.linalg.inv(Mc + Mreg)
    else:
        print("[globalCorrelation] Skip regularisation")
        left_hand_inverse = numpy.linalg.inv(Mc)
    del Mc

    # error = _errorCalc(im2, im1Def, im1, meshPaddingSlice)
    # print("\[globalCorrelation] Initial Error (abs) = ", error)

    # We try to solve Md=F
    # while error > 0.1 and error < errorIn:
    # while error > 0.1 and i <= maxIterations and error < errorIn:
    dxNorm = numpy.inf
    i = 0
    while dxNorm > convergenceCriterion and i < maxIterations:
        i += 1

        # This function returns globalVector (F) taking in im1Def and im2 and the gradients
        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run computeDICglobalVector: ", end="")
        right_hand_vector = numpy.zeros((3 * points.shape[0]), dtype="<f8")
        computeDICglobalVector(
            imTetLabel.astype("<u4"),
            im2Grad.astype("<f4"),
            im1Def.astype("<f4"),
            im2.astype("<f4"),
            connectivity.astype("<u4"),
            (points + displacements).astype("<f8"),
            right_hand_vector,
        )
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run solve: ", end="")

        # solve: we can use solve here for sake of precision (over computing
        # M^-1). However solve takes quite a lot of time for "small" meshes).

        if len(regularisation):
            right_hand_vector -= numpy.matmul(Mreg, displacements.ravel())
        dx = numpy.matmul(left_hand_inverse, right_hand_vector).astype("<f8")
        # dx_solve = numpy.linalg.solve(
        #     Mc,
        #     right_hand_vector
        # ).astype('<f8')
        # print(numpy.linalg.norm(dx - dx_solve))

        displacements += dx.reshape(points.shape[0], 3)
        dxNorm = numpy.linalg.norm(dx)
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        if medianFilterEachIteration:
            # use connectivity to filter
            print("[globalCorrelation] [newton] Median filter of displacements...")
            for nodeNumber in range(points.shape[0]):
                # get rows of connectivity (i.e., tets) which include this point
                connectedTets = numpy.where(connectivity == nodeNumber)[0]
                neighbourPoints = numpy.unique(connectivity[connectedTets])
                diff = numpy.median(displacements[neighbourPoints], axis=0) - displacements[nodeNumber]
                displacements[nodeNumber] += 0.5 * diff

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run labelTetrahedra: ", end="")

        imTetLabel = spam.label.labelTetrahedra(im1.shape, points + displacements, connectivity, nThreads=nThreads)
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run applyMeshTransformation: ", end="")
        im1Def = spam.DIC.applyMeshTransformation(
            im1,
            points,
            connectivity,
            displacements,
            imTetLabel=imTetLabel,
            nThreads=nThreads,
        )
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        if debugFiles:
            tifffile.imwrite(f"{prefix}-def-i{i:03d}.tif", im1Def)
            tifffile.imwrite(
                f"{prefix}-residual-cropped-i{i:03d}.tif",
                im1Def[meshPaddingSlice] - im2[meshPaddingSlice],
            )
            # tifffile.imwrite(f"{prefix}-imTetLabel-i{i:03d}.tif", imTetLabel)

            pointData = {"displacements": displacements, "initialDisplacements": initialDisplacements, "fluctuations": numpy.subtract(displacements, initialDisplacements)}

            # compute strain for each fields
            cellData = {}
            components = ["vol", "dev", "volss", "devss"]
            for fieldName, field in pointData.items():
                Ffield = spam.deformation.FfieldBagi(points, connectivity, field, verbose=False)
                decomposedFfield = spam.deformation.decomposeFfield(Ffield, components)
                for c in components:
                    cellData[f"{fieldName}-{c}"] = decomposedFfield[c]

            spam.helpers.writeUnstructuredVTK(
                points.copy(),
                connectivity.copy(),
                pointData=pointData,
                cellData=cellData,
                fileName=f"{prefix}-displacementFE-i{i:03d}.vtk",
            )

        # print("\t\[globalCorrelation] Error Out = %0.5f%%" % (error))
        # reshapedDispl = displacements.reshape(points.shape[0], 3)
        dMin = numpy.min(displacements, axis=0)
        dMed = numpy.median(displacements, axis=0)
        dMax = numpy.max(displacements, axis=0)
        strMin = f"Min={dMin[0]: .3f} {dMin[1]: .3f} {dMin[2]: .3f}"
        strMed = f"Med={dMed[0]: .3f} {dMed[1]: .3f} {dMed[2]: .3f}"
        strMax = f"Max={dMax[0]: .3f} {dMax[1]: .3f} {dMax[2]: .3f}"
        print(f"[globalCorrelation] [newton] i={i:03d}, displacements {strMin}, {strMed}, {strMax}, dx={dxNorm:.2f}")

    return displacements
