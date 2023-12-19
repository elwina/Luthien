/**
* Name: NewModel
* Based on the internal empty template. 
* Author: elwin
* Tags: 
*/
model NewModel

/* Insert your model definition here */
species building {
	// int Residential;
	int BID;
	// string restriction;
	rgb color <- #grey;
	int nb_total <- 0 update: length(people inside self);

	aspect base {
		draw shape color: color;
	}

}

species road {
	rgb color <- #black;
	float destruction_coeff <- 1.0;
	int ObjectID;

	aspect base {
		draw shape color: color;
	}

	int road_total <- 0;

	reflex update_color when: road_total > 0 {
		write road_total;
		color <- #red;
	}

	reflex update_color2 when: road_total = 0 {
		color <- #black;
	}
	
	

}

species people skills: [moving] { //wandering 
	rgb color <- #yellow;
	string agentname; // worker/child
	int id; // agent编号
	building init_place <- nil; // 初始位置
	list<int> start_hour <- []; // 启动时间
	list<int> start_min <- []; // 启动时间
	list<building> from_place <- []; // 从哪里
	list<building> to_place <- []; // 到哪里
	string status <- "stay"; // stay/moving
	int tripnum <- 0; // trip编号
	point the_target <- nil; // 目标点位
	reflex time_to_move when: current_hour = start_hour[tripnum] and current_min = start_min[tripnum] and status = "stay" {
		status <- "moving";
		the_target <- any_location_in(to_place[tripnum]);
		tripnum <- tripnum + 1;
		if tripnum >= length(start_hour) {
			tripnum <- 0;
		}

	}

	geometry last_edge <- nil;
	// move 根据道路权重图，找到一条前往target最近的道路
	reflex move when: the_target != nil {
		do goto target: the_target on: the_graph;
		if (current_edge != nil and last_edge != current_edge) {
			if (last_edge != nil) {
				ask road(last_edge) {
					self.road_total <- self.road_total - 1;
				}

			}

			ask road(current_edge) {
				self.road_total <- self.road_total + 1;
			}

			last_edge <- current_edge;
		}

		//path path_followed <- goto(target:the_target, on:the_graph, return_path: true,recompute_path:true);
		//道路的分段
		//		list<geometry> segments <- path_followed.segments;
		//		loop line over: segments {
		//			ask road(path_followed agent_from_geometry line) {
		//				// Value of destruction when a people agent takes a road
		//				// destruction_coeff <- destruction_coeff + (destroy * dist / shape.perimeter);
		//				// destruction_coeff <- 1.5 ;
		//			}
		//		}
		if the_target = location {
			the_target <- nil;
			status <- "stay";
			if (last_edge != nil) {
				ask road(last_edge) {
					self.road_total <- self.road_total - 1;
				}

				last_edge <- nil;
			}

		}

	}

	aspect base {
		draw circle(15) color: color border: #black;
	}

}

global {
	file shape_file_buildings <- file("$building_shapefile$");
	file shape_file_roads <- file("$road_shapefile$");
	csv_file csv_file_trip <- csv_file("$trip_csv_file$", true);

	float step <- 1 #mn;
	// 当前时刻  hour(24H) min(60MIN) 
	int current_hour update: (time / #hour) mod 24;
	int current_min update: (time / #minute) mod 60; // 人口行走的最小速度  1km/h 最大速度 5 km/h 
	float normal_speed <- 5.0 #km / #h;
	graph the_graph;

	init {
		create building from: shape_file_buildings with: [BID::int(read("$buildingID$"))] {}

		create road from: shape_file_roads with: [ObjectID::int(read("OBJECTID"))];

		map<road, float> weights_map <- road as_map (each::(each.shape.perimeter));
		the_graph <- as_edge_graph(road) with_weights weights_map;

		// the_graph <- as_edge_graph(road) ;
		int allnum <- $total_people$;

		create people number: allnum returns: workers {
			speed <- normal_speed;
			agentname <- "worker";
		}

		int i <- 0;
		loop worker over: workers {
			ask worker {
				self.id <- i;
			}

			i <- i + 1;
		}

		int cols <- 7;
		i <- 0;
		int nowid;
		loop str over: csv_file_trip.contents {
			if i mod cols = 0 {
				nowid <- str;
			}

			if i mod cols = 1 {
			}

			if i mod cols = 2 {
			}

			if i mod cols = 3 {
				int h <- str;
				ask workers[nowid] {
					self.start_hour <- self.start_hour + h;
				}

			}

			if i mod cols = 4 {
				int m <- str;
				ask workers[nowid] {
					self.start_min <- self.start_min + m;
				}

			}

			if i mod cols = 5 {
				int o <- str;
				building b <- (building where (each.BID = o))[0];
				ask workers[nowid] {
					self.from_place <- self.from_place + b;
				}

			}

			if i mod cols = cols - 1 {
				int d <- str;
				building b <- (building where (each.BID = d))[0];
				ask workers[nowid] {
					self.to_place <- self.to_place + b;
				}

				i <- 0;
			} else {
				i <- i + 1;
			}

		}

		loop worker over: workers {
			ask worker {
				self.init_place <- self.from_place[0];
				self.location <- any_location_in(self.init_place);
			}

		}

	}
	
	
	reflex save_result when: current_hour >0 {
//		list<int> cars_in_roads <- road collect each.road_total;
//		save cars_in_roads to: "save_data.csv" format: csv rewrite: (cycle = 0) ? true : false;
    ask road {
    save [int(self),current_hour,current_min,self.ObjectID,self.road_total] 
          to: "$saveCarsOnRoadFolder$"+string(current_hour)+"_"+string(current_min)+".csv" format: "csv" rewrite: (cycle = 0) ? true : false header: true;
    }       
	}

}

experiment road_traffic type: batch until: (cycle = 60 * 24) {
	parameter "Shapefile for the buildings:" var: shape_file_buildings category: "GIS";
	parameter "Shapefile for the roads:" var: shape_file_roads category: "GIS";
	output {
		monitor ticknow value: string(current_hour) + ":" + string(current_min);
		display city_display type: opengl {
			species building aspect: base;
			species road aspect: base;
			species people aspect: base;
		}

	}

}