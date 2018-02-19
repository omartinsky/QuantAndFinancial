// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 1: Differentiating simple function call */

namespace example1
{
    double f(double x)
    {
        double result = x*x;                     // Step 1
        return result;
    }

    void f_AD(double d_dresult, double x, double& d_dx)
    {
        double result = x * x;                   // Step 1

        // Reverse sweep
        d_dx += d_dresult * 2 * x;               // Step 1 reverse
    }

    void example1()
    {
        double x = 3;
        double y = f(x);                         // Step 1
        cout << "y = " << y << endl;

        // Reverse sweep
        double d_dy = 1;                         // Seed
        double d_dx = create_AD(x);
        f_AD(d_dy, x, d_dx);                     // Step 1 reverse
        cout << "dy_dx = " << d_dy << endl;

        // Numerical Checks
        CheckEqual(d_dx, FiniteDifference(std::bind(&f, _1), x));
    }
}
