#pragma once



std::tuple<double, Eigen::VectorXd>
inverse_power_method(Eigen::SparseMatrix<double, Eigen::ColMajor> &A,
                     Eigen::VectorXd &initial_guess,
                     double &shift,
                     double &tolerance,
                     size_t &max_iteration)

{  // https://netlib.org/utk/people/JackDongarra/etemplates/node96.html
    Eigen::VectorXd y = initial_guess / initial_guess.squaredNorm();

    Eigen::SparseMatrix<double, Eigen::ColMajor> identity(A.cols(), A.rows());

    Eigen::BiCGSTAB<Eigen::SparseMatrix<double>> solver;

    identity.setIdentity();

    for (size_t iteration=0; iteration<max_iteration; ++iteration)
    {
        Eigen::SparseMatrix<double, Eigen::ColMajor> Matrix = A - shift * identity;

        solver.compute(A);

        Eigen::VectorXd v = solver.solve(y);

        double theta = v.transpose() * y,
               quotient = (y - theta * v).squaredNorm() / abs(theta),
               eigen_value = shift + 1 / theta;

        Eigen::VectorXd eigen_vector = y / theta;

        if (quotient < tolerance)
            return std::make_tuple(eigen_value, eigen_vector);
    }


}


inline double get_norm_of_vector(Eigen::VectorXd &vector)
{
    return vector.squaredNorm();
}


inline double get_rayleigh_quotient(Eigen::VectorXd &X, Eigen::VectorXd &Y)
{
    Y.dot(X) / X.dot(X);
}