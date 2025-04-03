package cs5990;

import java.util.Random;

import repast.simphony.context.Context;
import repast.simphony.engine.environment.RunEnvironment;
import repast.simphony.engine.schedule.ScheduledMethod;
import repast.simphony.space.graph.Network;

public class Human
{
	public static final int STATE_SUSCEPTIBLE = 0;
	public static final int STATE_INFECTED = 1;
	public static final int STATE_RECOVERED = 2;

	private static Random random;

	private Context<Object> context;
	private Network<Object> network;
	private int state;
	private int tick;
	private int infectedTick;
	private double beta;
	private double gamma;

	static {
		random = new Random(System.nanoTime());
	}

	public Human(Context<Object> context, Network<Object> network, int state, double beta, double gamma) {
		this.context = context;
		this.network = network;
		this.state = state;
		this.tick = 0;
		this.beta = beta;
		this.gamma = gamma;
	}

	public int isSusceptible() {
		return this.state == Human.STATE_SUSCEPTIBLE ? 1 : 0;
	}

	public int isInfected() {
		return this.state == Human.STATE_INFECTED ? 1 : 0;
	}

	public int isRecovered() {
		return this.state == Human.STATE_RECOVERED ? 1 : 0;
	}

	@ScheduledMethod(start = 0, interval = 1)
	public void step() {
		if (this.state == Human.STATE_INFECTED && this.tick > this.infectedTick) {
			for (Object human : this.network.getAdjacent(this)) {
				if (Human.random.nextDouble() < this.beta) {
					((Human)human).tryBecomeInfected();
				}
			}

			if (Human.random.nextDouble() < this.gamma) {
				this.recover();
			}
		}

		++this.tick;
	}

	@ScheduledMethod(start = 0, interval = 10, pick = 1)
	public void terminateIfDone() {
		int susceptibleCount = 0;
		int infectedCount = 0;
		int recoveredCount = 0;
		int count = 0;

		for (Object object : this.context.getObjects(Human.class)) {
			Human human = (Human)object;

			susceptibleCount += human.isSusceptible();
			infectedCount += human.isInfected();
			recoveredCount += human.isRecovered();
			count += 1;
		}

		if (infectedCount == count || recoveredCount == count) {
			RunEnvironment.getInstance().endRun();
		}

		if (susceptibleCount < count && infectedCount == 0 && recoveredCount > 0) {
			RunEnvironment.getInstance().endRun();
		}
	}

	public boolean tryBecomeInfected() {
		if (this.state == Human.STATE_SUSCEPTIBLE) {
			this.state = Human.STATE_INFECTED;
			this.infectedTick = this.tick;
			return true;
		}

		return false;
	}

	public void recover() {
		if (this.state == Human.STATE_INFECTED) {
			this.state = Human.STATE_RECOVERED;
		}
	}
}
