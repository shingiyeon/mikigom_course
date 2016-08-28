#include <iostream>
#include "Graph.h"
#include <queue>

using namespace std;

#define Seoul 0
#define Busan 1
#define Incheon 2
#define Daegu 3
#define Daejeon 4
#define Gwangju 5
#define Ulsan 6
#define Suwon 7
#define Changwon 8
#define Seongnam 9
#define Goyang 10
#define Yongin 11
#define Bucheon 12
#define Ansan 13
#define Cheongju 14
#define Jeonju 15
#define Anyang 16
#define Cheonan 17
#define Namyangju 18
#define Pohang 19

#define Max_double 50000


const double Straight[20] = {0.00, 325.11, 27.00, 237.60, 139.96, 267.87, 307.05, 33.98, 296.45, 19.60, 16.42, 40.23, 19.96, 30.14, 112.3, 194.31, 19.25, 84.41, 22.39, 271.96};

const char* ind2name[20] = {"Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Ulsan", "Suwon", "Changwon", "Seongnam", "Goyang", "Youngin", "Bucheon", "Anan", "Cheongju", "Jeonju", "Anyang", "Cheonam", "Namyangju", "Pohang"};

void A_star(Graph *G, int start_node, int end_node){
	double smallest_function;
	int smallest_node;

	int n = G->getNumberOfNodes();
	double f[n], h[n], g[n];
	double cur_accum_dist = 0;

	for(int i=0;i<n;i++)
		g[i] = 0;
	
	bool visited[n];
	bool unvisited_child[n];
	for(int i=0;i<n;i++)
		visited[i] = false;
	int x = start_node;
	double route_len=0;

	cout<<"The shortest route from 'Gwangju' to 'Seoul' : ";

	while(true){
		cout << ind2name[x] << " -> ";
		visited[x] = true;

		for(int j=0;j<n;j++){
			g[j] = 0;
			f[j] = Max_double;
			h[j] = Max_double;
			unvisited_child[j] = false;
		}
		
		for(int j=0;j<n;j++){
			if (j==x) continue;
			if(G->isEdge(x, j) && !visited[j]){
				unvisited_child[j] = true;
				g[j] = G->getDistance(x, j);
				h[j] = Straight[j];
				f[j] = g[j]+Straight[j];
			}
		}

		smallest_node = 0;
		smallest_function = f[0];
		for(int j=0;j<n;j++){
			if (j==x) continue;
			if(f[j] < smallest_function && unvisited_child[j] == true){
				smallest_function = f[j];
				smallest_node = j;
			}
		}
		
		route_len = route_len + G->getDistance(x, smallest_node);

		x = smallest_node;

		if(x==end_node){
			cout << ind2name[x] <<endl;
			cout << "The shortest route length : " << route_len<<"km"<<endl;
			break;
		}
	}
}

int main(void){
	Graph Map(20);

	Map.setDistance(Seoul, Incheon, 36.53);
	Map.setDistance(Seoul, Goyang, 34.12);
	Map.setDistance(Seoul, Bucheon, 22.37);
	Map.setDistance(Seoul, Namyangju, 29.13);
	Map.setDistance(Seoul, Ansan, 36.69);
	Map.setDistance(Seoul, Suwon, 35.24);
	Map.setDistance(Seoul, Yongin, 41.84);
	Map.setDistance(Seoul, Seongnam, 20.60);
	Map.setDistance(Seoul, Anyang, 21.60);
	Map.setDistance(Incheon, Goyang, 32.83);
	Map.setDistance(Incheon, Ansan, 27.36);
	Map.setDistance(Incheon, Bucheon, 14.16);
	Map.setDistance(Anyang, Seongnam, 23.18);
	Map.setDistance(Anyang, Ansan, 14.45);
	Map.setDistance(Anyang, Bucheon, 20.83);
	Map.setDistance(Goyang, Namyangju, 52.14);
	Map.setDistance(Yongin, Seongnam, 32.03);
	Map.setDistance(Yongin, Suwon, 21.08);
	Map.setDistance(Yongin, Namyangju, 64.86);
	Map.setDistance(Suwon, Seongnam, 25.43);
	Map.setDistance(Suwon, Ansan, 19.79);
	Map.setDistance(Daejeon, Ansan, 145.00);
	Map.setDistance(Daejeon, Suwon, 125.21);
	Map.setDistance(Daejeon, Yongin, 122.15);
	Map.setDistance(Cheonan, Ansan, 74.51);
	Map.setDistance(Cheonan, Suwon, 54.72);
	Map.setDistance(Cheonan, Seongnam, 73.87);
	Map.setDistance(Cheongju, Seongnam, 119.09);
	Map.setDistance(Cheongju, Suwon, 100.10);
	Map.setDistance(Cheongju, Yongin, 93.34);
	Map.setDistance(Jeonju, Daejeon, 82.08);
	Map.setDistance(Jeonju, Cheonan, 122.95);
	Map.setDistance(Jeonju, Cheongju, 116.84);
	Map.setDistance(Gwangju, Jeonju, 103.64);
	Map.setDistance(Gwangju, Daegu, 189.10);
	Map.setDistance(Gwangju, Changwon, 206.00);
	Map.setDistance(Daegu, Daejeon, 141.14);
	Map.setDistance(Daegu, Cheongju, 175.26);
	Map.setDistance(Daegu, Pohang, 79.18);
	Map.setDistance(Daegu, Changwon, 95.76);
	Map.setDistance(Busan, Daegu, 121.83);
	Map.setDistance(Busan, Ulsan, 52.79);
	Map.setDistance(Busan, Changwon, 48.60);
	Map.setDistance(Ulsan, Pohang, 70.01);
	Map.setDistance(Ulsan, Daegu, 92.38);

	cout << "This Program is for computing the shortest rout from 'Gwangju' to 'Seoul'"<<endl;
	cout << "The program is implemented by 'A* algorithm'"<<endl;
	cout << "//////////////////////////////////"<<endl;

	A_star(&Map, Gwangju, Seoul);
	cout<< "////////////////////////////////"<<endl<<"The end of the program."<<endl;

	return 0;
}
