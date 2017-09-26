#pragma once

#include <string>
#include <vector>
#include <map>
#include <set>

using namespace std;

class       Node
{
public:
    int             id;
    string          name;
    vector<int>     inEdgeIdList;
    vector<int>     outEdgeIdList;
    vector<Node*>   inEdgeList;
    vector<Node*>   outEdgeList;
    vector<double>  featureList;
    vector<pair<int, int> > postIdList;

    Node();
    int             GetPostIdBySource(int sourcePostId);
    int             GetPostPosBySource(int sourcePostId);
    bool            HasOutEdge(int id);
};

class       Post
{
public:
    int             id;
    Node*           user;
    int             postTime;
    int             inactiveNeighbors;
    int             sourceId;
    string          name;
    Post*           sourcePost;
    vector<Post*>   influencedBy;
    Post();
};

class   DataLoader
{
public:
    int                 TIME_STEP;
    string              NETWORK_FILE_DIR;
    string              DIFFUSION_FILE_DIR;
    string              NETWORK_CONSTRAINT_FILE_DIR;
    string              PAGE_RANK_FILE_DIR;
    vector<Node*>       nodeList;
    vector<Post*>       postList;
    map<string, int>    userIdMap;
    map<string, int>    postIdMap;
    map<int, int>       sourceIdMap;
    
    DataLoader();
    int                 LoadData();
    int                 LoadNetwork(string fileDir);
    int                 LoadDiffusion(string fileDir);
    int                 LoadFeature(string fileDir);
    int                 GetUserId(const string& key);
    int                 GetPostId(const string& key);
    int                 GetOrInsertUserId(const string& key);
    int                 GetOrInsertPostId(const string& key);
    int                 GetOrInsertSourceId(const int key);
};
