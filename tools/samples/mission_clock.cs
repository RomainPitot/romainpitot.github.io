// Day → Night → Dawn → Debrief → Over, each on a deadline.
//
// Plain C# with the time passed in, like ContractVoteTally: the network
// wrapper (MissionManager) feeds it the server clock, and the tests feed it
// whatever numbers they want.
public class MissionClock
{
    public struct Durations
    {
        public double day;
        public double night;
        public double dawn;
        public double debrief;
    }

    readonly Durations durations;

    public MissionPhase Phase { get; private set; } = MissionPhase.None;

    // Anyone can press the truck button, even far too early: that's the joke
    // (GDD 13.1). Only meaningful during the day.
    public bool RequestNight(double now)
    {
        if (Phase != MissionPhase.Day) return false;

        Enter(MissionPhase.Night, now);
        return true;
    }

    // Moves at most one phase per call. Returns true when the phase changed.
    public bool Tick(double now)
    {
        if (Phase == MissionPhase.None || Phase == MissionPhase.Over) return false;
        if (now < Deadline) return false;

        Enter(Next(Phase), now);
        return true;
    }

    public double SecondsLeft(double now)
    {
        if (Phase == MissionPhase.None || Phase == MissionPhase.Over) return 0;
        return now >= Deadline ? 0 : Deadline - now;
    }
}
