#include <iostream>
#include <algorithm>
#include <vector>
#include <list>
#include "Graph.h"

using namespace std;

#define Gwangju 0
#define Busan 1
#define Incheon 2
#define Daegu 3
#define Daejeon 4
#define Seoul 5
#define Ulsan 6
#define Suwon 7
#define Changwon 8
#define Seongnam 9

const char* ind2name[10] = {"Gwangju", "Busan", "Incheon", "Daegu", "Daejeon", "Seoul", "Ulsan", "Suwon", "Changwon", "Seongnam"};

int n=10;
int start= Gwangju;

vector< vector < double >  > graph, dp, dp_cycle;
list<int> cycle(1, 0);
vector< vector < double > > subtable;
vector<bool> visited(n, false);

void init() {
	for ( int i = 0; i < n; ++i ){
		dp[ 1 << i ][ i ] = graph[ start ][ i ];
		dp_cycle[ 1 << i ][i] = graph[ start ][ i ];
	}
}


void subtables(vector< vector < double > > &subtable, const vector< vector < double > > &distance){
	subtable[1][0] = 0;
	for (int s = 3; s < (1<<n); s += 2) { 
		for (int j = 1; j < n; j++) {
			if (!(s & (1 << j)))
				continue;
			size_t t = s & ~(1 << j);
			for (int i = 0; i < n; i++) {
				if (s & (1 << i) && i != j && subtable[t][i] < 10e9) 
					subtable[s][j] = min(subtable[s][j], subtable[t][i] + distance[i][j]);
			}
		}
	}
}

double min_distance(int status, int x) {
	int best_i;
	double candidate_min;
	if ( dp[ status ][ x ] != -1 )
		return dp[ status ][ x ];
	int mask = 1 << x;
	dp[ status ][ x ] = 1e9;
	for ( int i = 0; i < n; ++i)
		if (i != x && ( status & ( 1 << i ) ) )
			dp[ status ][ x ] = min(dp[status][x], min_distance(status-mask, i) + graph[i][x]);
	return dp[ status ][ x ];
}


list<int> min_cycle(vector< vector < double > > $subtable, const vector< vector< double > > $distance){
	int s = (1<<n) -1;
	visited[0] = true;
	double min_distance;

	for(int i=0;i<n-1;i++){
		int next_node;
		min_distance = 10e9;

		for(int j = 0;j<n;j++){
			if(!visited[j] && subtable[s][j] + graph[cycle.back()][j] < min_distance){
				min_distance = subtable[s][j] + graph[cycle.back()][j];
				next_node = j;
			}
		}
		cycle.push_back(next_node);
		visited[next_node] =true;
		s &= ~(1 << next_node);
	}
	return cycle;
}

int main() {
	Graph Map(n);

	Map.setDistance(Seoul, Incheon, 36.53);
	Map.setDistance(Seoul, Busan, 325.11);
	Map.setDistance(Seoul, Incheon, 27.00);
	Map.setDistance(Seoul, Daegu, 237.60);
	Map.setDistance(Seoul, Daejeon, 139.96);
	Map.setDistance(Seoul, Gwangju, 267.87);
	Map.setDistance(Seoul, Ulsan, 307.05);
	Map.setDistance(Seoul, Suwon, 33.98);
	Map.setDistance(Seoul, Changwon, 296.45);
	Map.setDistance(Seoul, Seongnam, 19.60);
	Map.setDistance(Busan, Incheon, 330.4);
	Map.setDistance(Busan, Daegu, 88.09);
	Map.setDistance(Busan, Daejeon, 200.56);
	Map.setDistance(Busan, Gwangju, 202.06);
	Map.setDistance(Busan, Ulsan, 45.26);
	Map.setDistance(Busan, Suwon, 295.64);
	Map.setDistance(Busan, Changwon, 38.83);
	Map.setDistance(Busan, Seongnam, 305.85);
	Map.setDistance(Incheon, Daegu, 244.23);
	Map.setDistance(Incheon, Daejeon, 136.99);
	Map.setDistance(Incheon, Gwangju, 255.71);
	Map.setDistance(Incheon, Ulsan, 315.79);
	Map.setDistance(Incheon, Suwon, 35.72);
	Map.setDistance(Incheon, Changwon, 299.61);
	Map.setDistance(Incheon, Seongnam, 38.30);
	Map.setDistance(Daegu, Daejeon, 121.59);
	Map.setDistance(Daegu, Gwangju, 176.96);
	Map.setDistance(Daegu, Ulsan, 74.03);
	Map.setDistance(Daegu, Suwon, 209.01);
	Map.setDistance(Daegu, Changwon, 67.01);
	Map.setDistance(Daegu, Seongnam, 218.23);
	Map.setDistance(Daejeon, Gwangju, 140.84);
	Map.setDistance(Daejeon, Ulsan, 195.53);
	Map.setDistance(Daejeon, Suwon, 106.36);
	Map.setDistance(Daejeon, Changwon, 166.43);
	Map.setDistance(Daejeon, Seongnam, 123.64);
	Map.setDistance(Gwangju, Ulsan, 226.92);
	Map.setDistance(Gwangju, Suwon, 234.48);
	Map.setDistance(Gwangju, Changwon, 164.93);
	Map.setDistance(Gwangju, Seongnam, 255.40);
	Map.setDistance(Ulsan, Suwon, 280.22);
	Map.setDistance(Ulsan, Changwon, 65.86);
	Map.setDistance(Ulsan, Seongnam, 287.47);
	Map.setDistance(Suwon, Changwon, 265.63);
	Map.setDistance(Suwon, Seongnam, 22.40);
	Map.setDistance(Changwon, Seongnam, 277.59);

	graph = vector< vector< double > >( n, vector< double >( n ) );
	dp = vector< vector< double > >( 1 << n, vector< double >( n, -1 ) );
	dp_cycle = vector< vector< double > >(1 << n, vector< double >(n, -1 ) );
	subtable = vector< vector < double > >(1 << n, vector< double >(n, 10e9));

	for ( int i = 0; i < n; ++i )
		for ( int j = 0; j < n; ++j ) 
			graph[ i ][ j ] = Map.getDistance(i, j);

	cout << "This program is to implement dynamic programming for solving TSP." << endl;
	cout << "/////////////////////////////////////////////////////////////////" << endl<< endl;
	init();
	visited[0] = true;
	cout << "Total Traveling Distance : " << min_distance( ( 1 << n ) - 1, start )<<endl<<endl;

	subtables(subtable, graph);
	cycle = min_cycle(subtable, graph);

	list<int>::const_iterator it;

	cout << "Traveling Path : " <<endl;
	for(it = cycle.begin(); it != cycle.end(); ++it){cout << ind2name[*it] << " -> ";}
	cout << ind2name[0] << endl << endl;
	cout << "////////////////////// End of Program //////////////////////////" << endl;
	return 0;
}
