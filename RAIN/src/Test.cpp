#include "Util.h"
#include "Test.h"

#include <algorithm>
#include <sstream>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <complex>
#include <utility>
#include <fstream>
#include <iostream>
//#include <dirent.h>
//#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <cmath>
#include <random>



#define PI          3.141592653
#define EE          2.718281828459
#define MAXINT      10000000

using namespace std;

int                 Test::SampleRole(int u)
{
    int roleNum = model -> roleNum;
    double* p = new double[roleNum];
    for (int r = 0; r < roleNum; r ++)
    {
        p[r] = model -> theta[u][r];
    }
    // cumulate multinomial parameters
    for (int k = 1; k < roleNum; k ++) 
	    p[k] += p[k - 1];
    // scaled sample because of unnormalized p[]
    double s = ((double) random() / RAND_MAX) * p[roleNum - 1];

    int role = roleNum - 1;
    for (role = 0; role < roleNum - 1; role ++)
	    if (p[role] > s)
	        break;
    //printf("%.3lf %.3lf %d\n", p[K - 1], u, topic);
    delete[] p;
    return role;
}

int                 Test::SampleT(Node* user)
{
    int sum = 0;
    for (unsigned int i = 0; i < user -> postIdList.size(); i ++)
    {
        Post* post = model -> postList[user -> postIdList[i].second];
        sum += post -> postTime - post -> sourcePost -> postTime;
    }
    double t = (sum + 0.0) / user -> postIdList.size();
    if (t > model -> maxTime)
        t = model -> maxTime;
    return t;
}

int                 Test::SampleZ(Node* user)
{
    int sum = 0;
    for (unsigned int i = 0; i < user -> postIdList.size(); i ++)
    {
        Post* post = model -> postList[user -> postIdList[i].second];
        sum += post -> influencedBy.size();
    }
    double p = (user -> postIdList.size() + 0.0) / sum;
    double s = (double) random() / RAND_MAX;
    if (s <= p)
        return 1;
    return 0;
}


int                 Test::SampleT(int r)
{
    int t = 0;
    double p = model -> lambda[r];
    for (t = 0; t <= model -> maxTime; t ++)
    {
        double s = (double) random() / RAND_MAX;
        if (s <= p)
            return t;
    }
    return t;
}

int                 Test::SampleZ(int r)
{
    double p = model -> rho[r];
    double s = (double) random() / RAND_MAX;
    if (s <= p)
        return 1;
    return 0;
}

int                 Test::Simulation(int method)
{
    srand(time(0));
    int S = model -> S;
    for (int s = 0; s < S; s ++)
    {
        diffusionSize[s] = 0;
        diffusionDuration[s] = 0;
    }
    vector<pair<int, int> > activeList;
    set<int> activeSet;
    vector<Post*>* sourcePostList = new vector<Post*>[S];
    for (unsigned int i = 0; i < model -> postList.size(); i ++)
    {
        Post* post = model -> postList[i];
        if (post -> sourcePost -> id == post -> sourcePost -> sourcePost -> id)
            sourcePostList[post -> sourceId].push_back(post);
    }
    for (unsigned int i = 0; i < model -> postList.size(); i ++)
    {
        Post* post = model -> postList[i];
        if (post -> sourcePost -> id != post -> id)
            continue;
        int s = post -> sourceId;
        int postTime = post -> postTime;
        //printf("%d : %d ", s, (int) sourcePostList[s].size());
        diffusionSize[s] = 1;
        diffusionDuration[s] = 0;
        activeList.clear();
        activeSet.clear();
        activeList.push_back(make_pair(post -> user -> id, 0));
        activeSet.insert(post -> user -> id);
        for (unsigned int j = 0; j < sourcePostList[s].size(); j ++)
        {
            if (activeSet.count(sourcePostList[s][j] -> user -> id) > 0)
                continue;
            activeList.push_back(make_pair(sourcePostList[s][j] -> user -> id, sourcePostList[s][j] -> postTime - postTime));
            activeSet.insert(post -> user -> id);
        }
        int h = 0;
        while (h < (int) activeList.size())
        {
            Node* user = model -> nodeList[activeList[h].first];
            int currentTime = activeList[h].second;
            for (unsigned int j = 0; j < user -> inEdgeList.size(); j ++)
            {
                Node* target = user -> inEdgeList[j];
                if (activeSet.count(target -> id) > 0)
                    continue;
                int r = 0;
                if (method == 0)
                    r = SampleRole(user -> id);
                int t = 0;
                if (method == 0)
                    t = SampleT(r);
                if (method == 1)
                    t = SampleT(user);
                if (t == model -> maxTime)
                    continue;
                int z = 0;
                if (method == 0)
                    z = SampleZ(r);
                if (method == 1)
                    z = SampleZ(user);
                if (z == 1)
                {
                    activeList.push_back(make_pair(target -> id, currentTime + t));
                    activeSet.insert(target -> id);
                    if (currentTime + t > diffusionDuration[s])
                        diffusionDuration[s] = currentTime + t;
                }
            }
            h ++;
        }
        diffusionSize[s] = activeList.size();
    }
    return 0;
}

int                 Test::SizeAndDuration(int method)
{
    printf("Start Simulation!\n");
    int sampleTime = 1000;
    if (method == 1)
        sampleTime = 10;
    int S = model -> S;
    diffusionSize = new int[S];
    diffusionDuration = new int[S];
    int** totalSize = new int*[sampleTime];
    int** totalDuration = new int*[sampleTime];
    int proc = -1;
    for (int t = 0; t < sampleTime; t ++)
    {
        if (t * 100 / sampleTime > proc)
        {
            proc = t * 100 / sampleTime;
            printf("Simulation Processing %d%%...\n", proc);
        }
        Simulation(method);
        totalSize[t] = new int[S];
        totalDuration[t] = new int[S];
        for (int s = 0; s < S; s ++)
        {
            totalSize[t][s] = diffusionSize[s];
            totalDuration[t][s] = diffusionDuration[s];
        }
    }
    int* sizeCount = new int[model -> V];
    int* timeCount = new int[model -> maxTime];
    for (int v = 0; v < model -> V; v ++)
        sizeCount[v] = 0;
    for (int t = 0; t < model -> maxTime; t ++)
        timeCount[t] = 0;
    for (int s = 0; s < S; s ++)
    {
        int meanS = 0;
        int meanD = 0;
        for (int t = 0; t < sampleTime; t ++)
        {
            meanS += totalSize[t][s];
            meanD += totalDuration[t][s];
        }
        meanS /= sampleTime;
        meanD /= sampleTime;
        sizeCount[meanS] ++;
        timeCount[meanD] ++;
    }
    FILE* fout = fopen("simulation_results.txt", "w");
    double sum = sizeCount[100];
    for (int v = 99; v >= 1; v --)
    {
        sizeCount[v] += sizeCount[v + 1];
        sum += sizeCount[v];
    }
    for (int v = 1; v <= 100; v ++)
    {
        //fprintf(fout, "%d %.5lf\n", v, (sizeCount[v] + 0.0) / sum);
    }
    for (int v = 0; v < model -> V; v ++)
    {
        /*
        if (sizeCount[v] > 0)
            fprintf(fout, "%d %.5lf\n", v, (sizeCount[v] + 0.0) / S);
        */
    }
    //fprintf(fout, "\n");
    sum = timeCount[model -> maxTime - 1];
    for (int t = model -> maxTime - 2; t >= 0; t --)
    {
        timeCount[t] += timeCount[t + 1];
        sum += timeCount[t];
    }
    for (int t = 0; t < model -> maxTime; t ++)
    {
        //if (timeCount[t] > 0)
            fprintf(fout, "%d %.5lf\n", t, (timeCount[t] + 0.0) / sum);
    }
    fclose(fout);
    return 0;
}

int                 Test::TrueDuration()
{
    printf("Generating true duration!\n");
    FILE* fout = fopen("duration_truth.txt", "w");
    int S = model -> S;
    int* trueTime = new int[S];
    int* timeCount = new int[model -> maxTime];
    for (int s = 0; s < S; s ++)
        trueTime[s] = 0;
    for (int t = 0; t < model -> maxTime; t ++)
        timeCount[t] = 0;
    for (unsigned int i = 0; i < model -> postList.size(); i ++)
    {
        int t = model -> postList[i] -> postTime - model -> postList[i] -> sourcePost -> postTime;
        int sid = model -> postList[i] -> sourceId;
        if (t < model -> maxTime && t > trueTime[sid])
            trueTime[sid] = t;
    }
    for (int s = 0; s < S; s ++)
        timeCount[trueTime[s]] ++;
    int sum = timeCount[model -> maxTime - 1];
    for (int t = model -> maxTime - 2; t >= 0; t --)
    {
        timeCount[t] += timeCount[t + 1];
        sum += timeCount[t];
    }
    for (int t = 0; t < model -> maxTime; t ++)
    {
        fprintf(fout, "%d %.5lf\n", t, (timeCount[t] + 0.0) / sum);
    }
    fclose(fout);
    return 0;
}

int                 Test::TrueSize()
{
    FILE* fout = fopen("size_test_truth.txt", "w");
    int S = model -> S;
    int V = model -> V;
    int* truth_count = new int[S];
    int* truth = new int[V];
    set<int> *activeSet = new set<int>[S];
    for (int v = 0; v < V; v ++)
        truth[v] = 0;
    for (int s = 0; s < S; s ++)
    {
        truth_count[s] = 0;
        activeSet[s].clear();
    }
    for (unsigned int i = 0; i < model -> postList.size(); i ++)
    {
        Post* post = model -> postList[i];
        int sid = post -> sourceId;
        if (activeSet[sid].count(post -> user -> id) > 0)
            continue;
        truth_count[sid] ++;
        activeSet[sid].insert(post -> user -> id);
    }
    for (int s = 0; s < S; s ++)
        truth[truth_count[s]] ++;
    double sum = truth[100];
    for (int v = 99; v >= 1; v --)
    {
        truth[v] += truth[v + 1];
        sum += truth[v];
    }
    for (int v = 1; v <= 100; v ++)
    {
        fprintf(fout, "%d %.5lf\n", v, (truth[v] + 0.0) / sum);
    }
    for (int v = 0; v < V; v ++)
        if (truth[v] > 0)
        {
            //printf("%d %.5lf\n", v, (truth[v] + 0.0) / S);
            //fprintf(fout, "%d %.5lf\n", v, (truth[v] + 0.0) / S);
        }
    fclose(fout);
    return 0;
}


