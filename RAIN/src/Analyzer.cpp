#include "Util.h"
#include "Data.h"
#include "Analyzer.h"

#include <algorithm>
#include <sstream>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <utility>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <cmath>

#define MAXINT 10000000
#define MIN_POST_APPEARENCE 5

using namespace std;

double          Analyzer::EdgeWeight(int source, int target, int plan)
{
    double res;
    if (plan == 0)
        res = nodeList[source] -> outEdgeList.size();
    if (plan == 1)
        res = nodeList[target] -> inEdgeList.size();
    if (plan == 2)
        res = sqrt(nodeList[source] -> outEdgeList.size() * nodeList[target] -> inEdgeList.size());
    if (res > 0)
        return 1.0 / res;
    return 0;
}

int             Analyzer::CalcNetworkConstraint(int plan)
{
    shScoreList.clear();
    int proc = -1;
    for (unsigned int i = 0; i < nodeList.size(); i ++)
        shScoreList.push_back(0.0);
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        if ((int) (i * 100 / nodeList.size()) > proc)
        {
            proc = i * 100 / nodeList.size();
            printf("Processing %d%%...\n", proc);
        }
        Node* B = nodeList[i];
        for (unsigned int j = 0; j < B -> outEdgeList.size(); j ++)
        {
            Node* C = B -> outEdgeList[j];
            shScoreList[C -> id] += EdgeWeight(B -> id, C -> id, plan);
            //printf("%s -> %s: %.5lf\n", B -> name.c_str(), C -> name.c_str(), EdgeWeight(B -> id, C -> id, plan));
            for (unsigned int k = 0; k < C -> outEdgeList.size(); k ++)
            {
                Node* A = C -> outEdgeList[k];
                if (A -> id == B -> id)
                    continue;
                if (! B -> HasOutEdge(A -> id))
                    continue;
                int id = A -> id;
                double val = EdgeWeight(B -> id, C -> id, plan) * EdgeWeight(C -> id, A -> id, plan);
                //printf("%s %s %s: %.5lf\n", A -> name.c_str(), B -> name.c_str(), C -> name.c_str(), val);
                shScoreList[id] += val;         
            }
        }
    }
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        printf("%.5lf\n", shScoreList[i]);
        if (nodeList[i] -> inEdgeList.size() > 0)
            shScoreList[i] = pow(shScoreList[i], 2) / nodeList[i] -> inEdgeList.size();
        else
            shScoreList[i] = 1.0;
    }

    FILE* fout = fopen(("sh" + Util::Int2Str(plan) + ".txt").c_str(), "w");
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        fprintf(fout, "%s %.8lf\n", nodeList[i] -> name.c_str(), shScoreList[i]);
    }
    fclose(fout);
    return 0;
}

bool                shCmp(pair<string, double> a, pair<string, double> b)
{
    return a.second < b.second;
}

int                 Analyzer::LoadSH(const string& fileDir)
{
    vector<pair<string, double> > shList;
    vector<string> inputs = Util::ReadFromFile(fileDir.c_str());
    for (unsigned int i = 0; i < inputs.size(); i ++)
    {
        vector<string> tmp = Util::StringTokenize(inputs[i]);
        shList.push_back(make_pair(tmp[0], Util::String2Double(tmp[1])));
    }
    printf("#nodes: %d\n", (int) shList.size());
    sort(shList.begin(), shList.end(), shCmp);
    FILE* fout = fopen("sorted_nc_0.txt", "w");
    for (unsigned int i = 0; i < shList.size(); i ++)
    {
        fprintf(fout, "%s %.10lf\n", shList[i].first.c_str(), shList[i].second);
    }
    fclose(fout);
    return 0;
}

int                 Analyzer::ActiveNeighbor(int featureId, int pos)
{
    vector<double> features;
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        //printf("%s : %.5lf\n", nodeList[i] -> name.c_str(), nodeList[i] -> featureList[featureId]);
        features.push_back(-1 * pos * nodeList[i] -> featureList[featureId]);
    }
    sort(features.begin(), features.end());
    double T = features[features.size() * 0.1];
    T *= -1 * pos;
    printf("threshold: %.5lf\n", T);
    map<pair<int, int>, int> inactiveMap;
    vector<int> active;
    inactiveMap.clear();
    active.clear();
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        Node* node = post -> user;
        int total = 0;
        for (unsigned int j = 0; j < post -> influencedBy.size(); j ++)
        {
            Node* source = post -> influencedBy[j] -> user;
            if (source -> featureList[featureId] * pos >= T * pos)
                total ++;
        }
        for (unsigned int j = active.size(); (int) j <= total; j ++)
            active.push_back(0);
        active[total] ++;
        for (unsigned int j = 0; j < node -> inEdgeList.size(); j ++)
        {
            Node* target = node -> inEdgeList[j];
            pair<int, int> key = make_pair(post -> sourcePost -> id, target -> id);
            if (target -> GetPostIdBySource(post -> sourcePost -> id) == -1)
            {
                map<pair<int, int>, int>::iterator it = inactiveMap.find(key);
                if (it != inactiveMap.end())
                    it -> second ++;
                else
                    inactiveMap.insert(make_pair(key, 1));
            }
        }
    }
    vector<int> inactive;
    inactive.clear();
    for (map<pair<int, int>, int>::iterator it = inactiveMap.begin(); it != inactiveMap.end(); it++)
    {
        int idx = it -> second;
        for (unsigned int i = inactive.size(); (int) i <= idx; i ++)
            inactive.push_back(0);
        inactive[idx] ++;
    }
    FILE* fout = fopen(("analysis_" + Util::Int2Str(featureId) + ".txt").c_str(), "w");
    for (unsigned int i = 0; i < active.size() && i < inactive.size(); i ++)
    {
        if (active[i] > 0 || inactive[i] > 0)
        fprintf(fout, "%d %d %d\n", (int) i, active[i], inactive[i]);
    }
    fclose(fout);
    return 0;
}
