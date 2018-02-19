// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#include "helpers.h"
#include "example1-simple.h"
#include "example2-partialderivatives.h"
#include "example3-callstack.h"
#include "example4-cycles.h"
#include "example5-vectors1.h"
#include "example6-vectors2.h"

void header(string s)
{
    cout << "---------------" << endl;
    cout << s << endl;
}

int main()
{
    header("Example 1");
    example1::example1();
    header("Example 2");
    example2::example2();
    header("Example 3");
    example3::example3();
    header("Example 4");
    example4::example4();
    header("Example 5");
    example5::example5();
    header("Example 6");
    example6::example6();
}

