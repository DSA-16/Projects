package cs5990;

import java.util.ArrayList;
import java.util.Random;

import repast.simphony.context.Context;
import repast.simphony.context.space.graph.NetworkFactory;
import repast.simphony.context.space.graph.NetworkFactoryFinder;
import repast.simphony.engine.environment.RunEnvironment;
import repast.simphony.engine.schedule.ScheduledMethod;
import repast.simphony.dataLoader.ContextBuilder;
import repast.simphony.parameter.Parameters;
import repast.simphony.space.graph.Network;

public class Main implements ContextBuilder<Object>
{
	private static Random random;

	static {
		random = new Random(System.nanoTime());
	}

	@Override
	public Context build(Context<Object> context) {
		Parameters params = RunEnvironment.getInstance().getParameters();

		int humanCount = params.getInteger("populationSize");
		int initialInfectedCount = (int)(humanCount * params.getDouble("initialInfectedProportion"));
		int networkMode = params.getInteger("networkMode");
		int wsDegree = params.getInteger("wsDegree");
		double wsRewiringParameter = params.getDouble("wsRewiringParameter");
		int baCoreSize = params.getInteger("baCoreSize");
		int baNewEdges = params.getInteger("baNewEdges");
		double beta = params.getDouble("beta");
		double gamma = params.getDouble("gamma");

		context.setId("cs5990");

		NetworkFactory networkFactory = NetworkFactoryFinder.createNetworkFactory(null);
		Network<Object> network = networkFactory.createNetwork("network", context, false);

		ArrayList<Human> humans = new ArrayList<>();

		for (int i = 1; i <= humanCount; ++i) {
			Human human = new Human(
				context,
				network,
				i <= initialInfectedCount ? Human.STATE_INFECTED : Human.STATE_SUSCEPTIBLE,
				beta,
				gamma
			);

			humans.add(human);
			context.add(human);
		}

		switch (networkMode) {
			case 0:
				this.buildBarabasiAlbertNetwork(network, humans, humans.size(), 0);
				break;

			case 1:
				this.buildWattsStrogatzNetwork(network, humans, wsDegree, wsRewiringParameter);
				break;

			case 2:
				this.buildBarabasiAlbertNetwork(network, humans, baCoreSize, baNewEdges);
				break;
		}

		RunEnvironment.getInstance().endAt(2000);

		return context;
	}

	private void buildWattsStrogatzNetwork(Network<Object> network, ArrayList<Human> humans, int degree, double rewiringParameter) {
		int size = humans.size();
		int[][] adjacencyList = new int[size][];

		for (int i = 0; i < size; ++i) {
			adjacencyList[i] = new int[degree / 2];

			for (int j = 0; j < degree / 2; ++j) {
				adjacencyList[i][j] = (i + j) % size;
			}
		}

		for (int i = 0; i < size; ++i) {
			for (int j = 0; j < degree / 2; ++j) {
				if (Main.random.nextDouble() <= rewiringParameter) {
					while (true) {
						int node = Main.random.nextInt(size);

						if (node == i) {
							continue;
						}
						if (this.listContains(adjacencyList[i], node)) {
							continue;
						}
						if (this.listContains(adjacencyList[node], i)) {
							continue;
						}

						adjacencyList[i][j] = node;

						break;
					}
				}
			}
		}

		for (int i = 0; i < size; ++i) {
			for (int j = 0; j < degree / 2; ++j) {
				network.addEdge(humans.get(i), humans.get(adjacencyList[i][j]));
			}
		}
	}

	private void buildBarabasiAlbertNetwork(Network<Object> network, ArrayList<Human> humans, int coreSize, int newEdges) {
		int size = humans.size();
		int[] degrees = new int[size];
		int degreesSum = 0;

		for (int i = 0; i < coreSize; ++i) {
			for (int j = i + 1; j < coreSize; ++j) {
				network.addEdge(humans.get(i), humans.get(j));
			}

			degrees[i] = coreSize - 1;
			degreesSum += coreSize - 1;
		}

		for (int i = coreSize; i < size; ++i) {
			for (int j = 0; j < newEdges; ++j) {
				int selectedNode = this.selectRandomNode(degrees, degreesSum);

				network.addEdge(humans.get(i), humans.get(selectedNode));

				degrees[selectedNode] += 1;
				degreesSum += 1;
			}

			degrees[i] = newEdges;
			degreesSum += newEdges;
		}
	}

	private int selectRandomNode(int[] degrees, int degreesSum) {
		int random = Main.random.nextInt(degreesSum);

		for (int i = 0; i < degrees.length; ++i) {
			random -= degrees[i];

			if (random < 0.0) {
				return i;
			}
		}

		return 0;
	}

	private boolean listContains(int[] list, int value) {
		for (int i = 0; i < list.length; ++i) {
			if (list[i] == value) {
				return true;
			}
		}

		return false;
	}
}
