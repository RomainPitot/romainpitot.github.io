// What the swarm needs to know about the level. Real game: physics colliders
// (PhysicsSwarmWorld). Tests: a fake.
public interface ISwarmWorld
{
    // Can a roach crawling at `height` go from A to B in a straight line?
    bool Blocked(Vector2 from, Vector2 to, float height, out Vector2 normal);

    // Height of the highest surface at p below `probeTop` (floor = 0).
    float SurfaceHeight(Vector2 p, float probeTop);
}

// The cockroach swarm, simulated on every PC.
//
// Only events travel over the network: "N roaches appear here" (seeded, so
// every PC places them the same way), "kill what's in this cone", "kill what's
// in this circle". After that each PC moves its own roaches; small
// differences between PCs don't matter for a crowd.
//
// Plain C# on arrays, no per-roach objects: hundreds must stay cheap.
public class SwarmSim
{
    public const int Capacity = 400;

    public struct Settings
    {
        public float wanderSpeed;
        public float fleeSpeed;
        public float playerFearRadius;   // roaches flee agents and UV light...
        public float boldFraction;       // ...except the bold ones that chase them
        public float climberFraction;    // share that climbs the furniture they bump into
        public float maxClimb;           // furniture yes, walls no
    }
}
