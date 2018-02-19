// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 4: Differentiating cycles  */

namespace example4
{
    double f(double x, int n)
    {
        double result = 1;
        for (int i = 0; i < n; ++i)
            result *= x + i;                     // Step 1
        return result;
    }

    void f_AD(double d_dresult, double x, int n, double& d_dx)
    {
        // We need to cache history of results for reverse sweep
        vector<double> results;
        results.reserve(n);     

        double result = 1;
        for (int i = 0; i < n; ++i)
        {
            results.push_back(result);
            result *= x + i;                     // Step 1
        }

        // Reverse sweep
        for (int i = n - 1; i >= 0; --i)
        {
            d_dx += d_dresult * results[i];
            d_dresult = d_dresult * (x + i);     // Step 1 Reverse
        }

        /*
        Illustration of manual calculation for n=3
        double r0 = 1;                           // Step 0
        double r1 = r0*(x+0) = r0*x + r0*0;      // Step 1
        double r2 = r1*(x+1) = r1*x + r1*1;      // Step 2
        double r3 = r2*(x+2) = r2*x + r2*2;      // Step 3

        // Reverse sweep
        double d_dr3 = 1;
        double d_dx = 0;

        d_dx += d_dr3 * r2;                      // Step 3 reverse, derivative w.r.t. "x"
        double d_dr2 = create_AD(r2);            
        d_dr2 += d_dr3 * (x + 2);                // Step 3 reverse, derivative w.r.t. "r2"             

        d_dx += d_dr2 * r1;                      // Step 2 reverse, derivative w.r.t. "x"       
        double d_dr1 = create_AD(r1);
        d_dr1 += d_dr2 * (x + 1);                // Step 2 reverse, derivative w.r.t. "r1" 

        d_dx += d_dr1 * r0;                      // Step 1 reverse, derivative w.r.t. "x" 
        double d_dr0 = create_AD(r0);
        d_dr1 += d_dr1 * (x + 0);                // Step 1 reverse, derivative w.r.t. "r0" 
        */ 
    }

    void example4()
    {
        double x = 4;
        int n = 3;
        double y = f(x, n);                      // Step 1
        cout << "y = " << y << endl;
        
        // Reverse sweep
        double d_dy = 1;                         // Seed
        double d_dx = create_AD(x);
        f_AD(d_dy, x, n, d_dx);                  // Step 1 reverse
        cout << "dy_dx = " << d_dx << endl;

        // Numerical Checks
        CheckEqual(d_dx, FiniteDifference(std::bind(&f, _1, n), x));
    }
}
