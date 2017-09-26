#include "Util.h"
#include "Data.h"

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

Node::Node()
{
    inEdgeList.clear();
    outEdgeList.clear();
    featureList.clear();
    postIdList.clear();
}

Post::Post()
{
    influencedBy.clear();
}

DataLoader::DataLoader()
{
    TIME_STEP = 1;
    userIdMap.clear();
    postIdMap.clear();
}

int             Node::GetPostPosBySource(int sourcePostId)
{
    int l = 0;
    int r = postIdList.size() - 1;
    int pos = -1;
    while (l <= r)
    {
        int mid = (l + r) / 2;
        if (postIdList[mid].first == sourcePostId)
        {
            pos = mid;
            break;
        }
        if (postIdList[mid].first < sourcePostId)
            l = mid + 1;
        else
            r = mid - 1;
    }
    while (pos > 0 && postIdList[pos - 1].first == sourcePostId)
        pos --;
    return pos;
}

int             Node::GetPostIdBySource(int sourcePostId)
{
    int res = GetPostPosBySource(sourcePostId);
    if (res == -1)
        return -1;
    return postIdList[res].second;
}

bool            Node::HasOutEdge(int id)
{
    int l = 0;
    int r = outEdgeIdList.size() - 1;
    while (l <= r)
    {
        int mid = (l + r) / 2;
        if (outEdgeIdList[mid] == id)
            return true;
        if (outEdgeIdList[mid] < id)
            l = mid + 1;
        else
            r = mid - 1;
    }
    return false;
}

int             DataLoader::GetUserId(const string& key)
{
    map<string, int>::iterator it = userIdMap.find(key);
    if (it != userIdMap.end())
        return it -> second;
    return -1;
}

int				DataLoader::GetOrInsertUserId(const string& key)
{
    map<string, int>::iterator it = userIdMap.find(key);
    if (it != userIdMap.end())
        return it -> second;
    int id = (int) nodeList.size();
    Node* user = new Node();
    user -> id = id;
    user -> name = key;
    nodeList.push_back(user);
    userIdMap.insert(make_pair(key, id));
	return id;
}

int             DataLoader::GetPostId(const string& key)
{
    map<string, int>::iterator it = postIdMap.find(key);
    if (it != postIdMap.end())
        return it -> second;
    return -1;
}

int             DataLoader::GetOrInsertSourceId(const int key)
{
    map<int, int>::iterator it = sourceIdMap.find(key);
    if (it != sourceIdMap.end())
        return it -> second;
    int id = sourceIdMap.size();
    sourceIdMap.insert(make_pair(key, id));
	return id;
 
}

int             DataLoader::GetOrInsertPostId(const string& key)
{
    map<string, int>::iterator it = postIdMap.find(key);
    if (it != postIdMap.end())
        return it -> second;
    Post* post = new Post();
    int id = (int) postList.size();
    post -> id = id;
    post -> name = key;
    post -> sourcePost = NULL;
    post -> postTime = 0;
    postList.push_back(post);
    postIdMap.insert(make_pair(key, id));
	return post -> id;
}

int             DataLoader::LoadNetwork(string fileDir)
{
    vector<string> inputs = Util::ReadFromFile(fileDir.c_str());
    int proc = -1;
    for (unsigned int i = 0; i < inputs.size(); i ++)
    {
        if (inputs[i].length() <= 1)
            continue;
        //printf("%s", inputs[i].c_str());
        //if (i > 1000)
        //    break;
        if ((int) (i * 100 / inputs.size()) > proc)
        {
            proc = int (i * 100 / inputs.size());
            if (proc % 10 == 0)
                printf("Loading %d%% networking data ...\n", proc);
        }
        vector<string> tokens = Util::StringTokenize(inputs[i]);
        if (tokens.size() == 0)
            continue;
        int source = GetOrInsertUserId(tokens[0]);
        nodeList[source] -> name = tokens[0];
        for (unsigned int j = 1; j < tokens.size(); j ++)
        {
            int target = GetOrInsertUserId(tokens[j]);
            nodeList[source] -> outEdgeList.push_back(nodeList[target]);
            nodeList[target] -> inEdgeList.push_back(nodeList[source]);
            //nodeList[target] -> name = tokens[j];
        }
    }
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        Node* node = nodeList[i];
        nodeList[i] -> outEdgeIdList.clear();
        for (unsigned int j = 0; j < node -> outEdgeList.size(); j ++)
            nodeList[i] -> outEdgeIdList.push_back(node -> outEdgeList[j] -> id);
        sort(nodeList[i] -> outEdgeIdList.begin(), nodeList[i] -> outEdgeIdList.end());
    }
    /*
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        printf("%s : %d\n", nodeList[i] -> name.c_str(), (int) nodeList[i] -> outEdgeList.size());
    }
    */
    printf("Load %d user in total.\n", (int) nodeList.size());
    return 0;
}

int             DataLoader::LoadFeature(string fileDir)
{
    vector<string> inputs = Util::ReadFromFile(fileDir.c_str());
    for (unsigned int i = 0; i < inputs.size(); i ++)
    {
        vector<string> tokens = Util::StringTokenize(inputs[i]);
        int uid = GetUserId(tokens[0]);
        if (uid == -1)
            continue;
        double val = Util::String2Double(tokens[1]);
        nodeList[uid] -> featureList.push_back(val + 1e-10);
    }
    return 0;
}

bool            pairFirstCmp(pair<int, int> a, pair<int, int> b)
{
    return a.first < b.first  || (a.first == b.first && a.second < b.second);
}

bool            inputCmp(string a, string b)
{
    vector<string> tokens_a = Util::StringTokenize(a);
    vector<string> tokens_b = Util::StringTokenize(b);
    return (Util::String2Int(tokens_a[1]) < Util::String2Int(tokens_b[1]));
}

int             DataLoader::LoadDiffusion(string fileDir)
{
    vector<string> inputs = Util::ReadFromFile(fileDir.c_str());
    //sort(inputs.begin(), inputs.end(), inputCmp);
    //printf("%s\n", inputs[0].c_str());
    int nofound = 0;
    for (unsigned int i = 0; i < inputs.size(); i ++)
    {
        //if (i > 1000)
        //    break;
        if (inputs[i].length() <= 1)
            continue;
        vector<string> tokens = Util::StringTokenize(inputs[i]);
        /*
        if (! (tokens[3].length() > 1 && tokens[4].length() > 1 && tokens[5].length() > 1 && tokens[6].length() > 1))
            continue;
        */
        Post* post = new Post();
        int pid = (int) postList.size();
        int t = Util::String2Int(tokens[1]);
        int uid = GetUserId(tokens[2]);
        if (uid == -1)
        {
            nofound ++;
            continue;
        }
        post -> id = pid;
        post -> name = tokens[0];
        post -> user = nodeList[uid];
        post -> postTime = t / TIME_STEP;
        int sid = post -> id;
        if (tokens[3].length() > 1)
            sid = GetPostId(tokens[3]);
        if (tokens[5].length() > 1 && GetPostId(tokens[5]) == -1)
            continue;
        if (sid == -1)
            continue;
        post -> sourceId = GetOrInsertSourceId(sid);
        postIdMap.insert(make_pair(tokens[0], pid));
        postList.push_back(post);
        post -> sourcePost = postList[sid];
        //postList.push_back(post);
        /*
        if (post -> id == 49690 || post -> id == 7127)
            printf("%s %d %d %d\n", post -> name.c_str(), post -> postTime, sid, nodeList[uid] -> GetPostIdBySource(sid));
        */
        nodeList[uid] -> postIdList.push_back(make_pair(sid, post -> id));
    }
    //printf("Missed %d posts.\n", (int) (inputs.size() - postList.size()));
    // influencer candidates
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        sort(nodeList[i] -> postIdList.begin(), nodeList[i] -> postIdList.end(), pairFirstCmp);
    }
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        post -> influencedBy.clear();
        Node* user = post -> user;
        if (postList[i] -> sourcePost -> id != postList[i] -> id)
        {
            for (unsigned int j = 0; j < user -> outEdgeList.size(); j ++)
            {
                Node* source = user -> outEdgeList[j];
                //printf("%s %s\n", user -> name.c_str(), source -> name.c_str());
                int pid = source -> GetPostIdBySource(post -> sourcePost -> id);
                int sourcePostTime = -1;
                if (pid != -1)
                    sourcePostTime = postList[pid] -> postTime;
                if (pid == -1)
                    continue;
                if (sourcePostTime <= post -> postTime)
                    post -> influencedBy.push_back(postList[pid]);
            }
            //printf("%d\n", (int) post -> influencedBy.size());
        }
        postList[i] -> inactiveNeighbors = 0;
        for (unsigned int j = 0; j < user -> inEdgeList.size(); j ++)
        {
            Node* target = user -> inEdgeList[j];
            int p = target -> GetPostIdBySource(post -> sourcePost -> id);
            if (p == -1)
            {
                postList[i] -> inactiveNeighbors ++;
            }
        }
    }

    // debug: print out all posts info
    int influencedByCnt = 0;
    int repostCnt = 0;
    int errorCnt = 0;
    vector<Post*> tmpPostList;
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        if (post -> sourcePost -> id != post -> id)
        {
            influencedByCnt += post -> influencedBy.size();
            repostCnt ++;
        }
        if (post -> influencedBy.size() == 0 && post -> sourcePost -> id != post -> id)
        {
            errorCnt ++;
            //printf("id: %d, name: %s, user: %d, #influencer: %d\n", post -> id, post -> name.c_str(), post -> user -> id, (int) post -> influencedBy.size());
        }
        else
        {
            tmpPostList.push_back(post);
        }
    }
    printf("Load %d posts in total.\n", (int) postList.size());
    printf("#Posts have no influencer: %d\n", errorCnt);
    printf("Average influenced by number: %.5lf (%d/%d)\n", (influencedByCnt + 0.0) / (repostCnt + 0.0), influencedByCnt, repostCnt);
    return 0;
}

int         DataLoader::LoadData()
{
    printf("######## Start loading data ########\n");
    userIdMap.clear();
    postIdMap.clear();
    sourceIdMap.clear();
    LoadNetwork(NETWORK_FILE_DIR);
    LoadDiffusion(DIFFUSION_FILE_DIR);
    LoadFeature(NETWORK_CONSTRAINT_FILE_DIR);
    int a = 0;
    int b = 0;
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        if (nodeList[i] -> featureList.size() == 0)
        {
            //nodeList[i] -> featureList.push_back(1e-5);
            nodeList[i] -> featureList.push_back(1.0);
            a ++;
        }
        //nodeList[i] -> featureList[0] = 0;
        //nodeList[i] -> featureList[0] *= 100;
    }
    LoadFeature(PAGE_RANK_FILE_DIR);
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        if (nodeList[i] -> featureList.size() < 2)
        {
            nodeList[i] -> featureList.push_back(0);
            b ++;
        }
        //nodeList[i] -> featureList[1] = 0;  
        //nodeList[i] -> featureList[1] /= 100;
        //nodeList[i] -> featureList[1] = 1.0 / (1 + exp(-1 * nodeList[i] -> featureList[1]));
    }
    printf("Missing %.5lf%% (%d / %d) PageRank.\n", (b + 0.0) * 100 / nodeList.size(), b, (int) nodeList.size());
    printf("Missing %.5lf%% (%d / %d) NetworkConstraint.\n", (a + 0.0) * 100 / nodeList.size(), a, (int) nodeList.size());
    printf("Dataset is ready!\n");
    return 0;
}

