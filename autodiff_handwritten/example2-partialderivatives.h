// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 2: Partial derivatives of a function with two arguments */

namespace example2
{

    double f(double x1, double x2)
    {
        double tmp1 = log(x1);                   // Step 1
        double tmp2 = x2 * x2* x2;               // Step 2
        double result = tmp1 + tmp2;             // Step 3
        return result;
    }

    void f_AD(double d_dresult, double x1, double x2, double& d_dx1, double& d_dx2)
    {
        double t1 = log(x1);                     // Step 1
        double t2 = x2 * x2 * x2;                // Step 2
        double result = t1 + t2;                 // Step 3

        // Reverse sweep
        double d_dt1 = create_AD(t1);
        double d_dt2 = create_AD(t2);
        d_dt1 += d_dresult * 1;                  // Step 3 reverse, derivative w.r.t. "t1"
        d_dt2 += d_dresult * 1;                  // Step 3 reverse, derivative w.r.t. "t2"
                                                                                      
        d_dx2 += d_dt2 * 3 * x2 * x2;            // Step 2 reverse, derivative w.r.t. "x2"
                                                                                      
        d_dx1 += d_dt1 * 1 / x1;                 // Step 1 reverse, derivative w,r.t. "x1"
    }

    void example2()
    {
        double x1 = 3;
        double x2 = 4;
        double y = f(x1, x2);                    // Step 1
        cout << "y = " << y << endl;

        // Reverse sweep
        double d_dy = 1;                         // Seed
        double d_dx1 = create_AD(x1);
        double d_dx2 = create_AD(x2);
        f_AD(d_dy, x1, x2, d_dx1, d_dx2);        // Step 1 reverse, derivative w.r.t. "x1" and "x2"
        cout << "dy_dx1 = " << d_dx1 << endl;
        cout << "dy_dx2 = " << d_dx2 << endl;

        // Numerical Checks
        CheckEqual(d_dx1, FiniteDifference(std::bind(&f, _1, x2), x1));
        CheckEqual(d_dx2, FiniteDifference(std::bind(&f, x1, _1), x2));
    }
}
