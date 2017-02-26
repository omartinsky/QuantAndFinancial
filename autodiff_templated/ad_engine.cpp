// Copyright © 2016 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#include "ad_engine.hpp"
#include <assert.h>

//////////////////////////////////////////////////////////////
// ADDouble

ADDouble::ADDouble(ADEngine& engine, double value)
    : _engine(engine)
    , _value(value)
{
    _id = engine._id_counter++;
#ifdef AD_ENABLE_LOGGING
    cout << "Creating new variable AD" << _id << " = " << value << endl;
#endif
    engine._variables.insert(make_pair(_id, *this));
}

//////////////////////////////////////////////////////////////
// ADEngine

void ADEngine::add_direct_derivative(const ADDouble& of, const ADDouble& wrt, double value)
{
#ifdef AD_ENABLE_LOGGING
    cout << "    " << logging::getVariableName(of) << "/d" 
        << logging::getVariableName(wrt) << " += " << value << endl;
#endif
    _derivatives[of._id][wrt._id] += value;
}

double ADEngine::get_derivative(const ADDouble& of, const ADDouble& wrt)
{
    return get_derivative(of._id, wrt._id);
}

double ADEngine::get_derivative(NodeId of, NodeId wrt)
{
    if (wrt == of)
        return 1.0;     // d variable w.r.t. self is 1.0 by definition

    DerivativeTable::const_iterator it = _derivatives.find(of);
    if (it == _derivatives.end())
        return 0.0;
    double val = 0;
    for (const map<NodeId, double>::value_type& direct_derivative : it->second)
    {
        if (direct_derivative.first == wrt)
            val += direct_derivative.second;
        else
            val += direct_derivative.second * get_derivative(direct_derivative.first, wrt);
    }
#ifdef AD_ENABLE_LOGGING
    cout << "Calculating derivative dVAR" << of << "/dVAR" << wrt << " = " << val << endl;
#endif

    return val;
}