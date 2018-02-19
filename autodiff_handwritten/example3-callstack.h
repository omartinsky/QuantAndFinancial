// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 3: Differentiating call stack (function calling other functions) */

namespace example3
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

    double g(double x, double p)
    {
        double t1 = 5 * f(x);                    // Step 1
        double t2 = 4 * f(p);                    // Step 2
        double result = t1 * t2;                 // Step 3
        return result;
    }

    void g_AD(double d_dresult, double x, double p, double& d_dx)
    {
        double t1 = 5 * f(x);                    // Step 1
        double t2 = 4 * f(p);                    // Step 2
        double result = t1 * t2;                 // Step 3

        // Reverse sweep
        double d_dt1 = create_AD(t1);
        double d_dt2 = create_AD(t2);
        d_dt1 = d_dresult * t2;                  // Step 3 reverse, derivative w.r.t. "t1"
        d_dt2 = d_dresult * t1;                  // Step 3 reverse, derivative w.r.t. "t2"

        // Derivative with w.r.t. "p"  is not necessary, skipping Step 2 reverse
        // double d_dp = create_AD(p);
        // f_AD(4 * d_dt2, p, d_dp); 

        f_AD(5 * d_dt1, x, d_dx);               //  Step 1 reverse
    }

    void example3()
    {
        double x = 4;
        double p = 5;
        double y = g(x, p);                       // Step 1
        cout << "y = " << y << endl;

        // Reverse sweep
        double d_dy = 1;                          // Seed
        double d_dx = create_AD(x);               
        g_AD(d_dy, x, p, d_dx);                   // Step 1 reverse, derivative w.r.t. "x1"
        cout << "dy_dx = " << d_dx << endl;

        // Numerical Checks
        CheckEqual(d_dx, FiniteDifference(std::bind(&g, _1, p), x));
    }
}
