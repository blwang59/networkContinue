#pragma once

#include "Data.h"
#include <string>
#include <vector>
#include <map>
#include <set>

using namespace std;

class       Analyzer
{
public:
    vector<Node*>       nodeList; 
    vector<Post*>       postList;
    vector<double>      shScoreList;
    int                 ActiveNeighbor(int featureId, int pos);
    int                 LoadSH(const string& fileDir);
    int                 CalcNetworkConstraint(int plan);
    double              EdgeWeight(int source, int target, int plan);
};
