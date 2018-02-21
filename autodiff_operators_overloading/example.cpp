// Copyright © 2016 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#include "ad_engine.hpp"

#include <iomanip>
#include "unit_tests.hpp"

using namespace std;

template <typename T>
T f(T x0, T x1)
{
    return log(x0) + x1 * x1 * x1;
}

void example1()
{
    ADEngine e;   // Create AD engine with derivatives tree

    // Register independent variables. Later, we will request derivative of the result
    // with respect to these variables
    ADDouble x0(e, 3);
    ADDouble x1(e, 4);

    // Do the calculation 
    ADDouble y = f(x0, x1);
    cout << "y = " << y.get_value() << endl;

    // Apply chain rule to derivatives in calculation tree
    cout << endl;
    cout << "*** Automatic differentiation" << endl;
    cout << "dy_dx0 = " << e.get_derivative(y, x0) << endl;
    cout << "dy_dx1 = " << e.get_derivative(y, x1) << endl;

    // Finite difference method
    double d = 1e-6;
    cout << endl;
    cout << "*** Finite difference method" << endl;
    cout << "dy_dx0 = " << (f(3. + d, 4.) - f(3. - d, 4.)) / (2 * d) << endl;
    cout << "dy_dx1 = " << (f(3., 4. + d) - f(3., 4. - d)) / (2 * d) << endl;
}

void main()
{
#if 0
    unit_tests();
#endif

    example1();
}