// Picks where the nest is this time and which clues are on site.
// Plain C# with the randomness injected, so the draw is testable and the
// server is the only one rolling dice.
public static class NestDraw
{
    public struct Result
    {
        public int nest;
        public List<int> clues;
    }

    // clueNest[i] = index of the nest clue i leads to, or -1 for a decoy.
    // Every clue of the drawn nest is shown (no single clue is enough, GDD 4:
    // they have to be crossed), plus a few decoys so a clue alone proves nothing.
    public static Result Draw(Random rng, int nestCount, IList<int> clueNest, int decoysToShow)
    {
        Result result = new Result { nest = -1, clues = new List<int>() };
        if (rng == null || nestCount <= 0 || clueNest == null) return result;

        result.nest = rng.Next(nestCount);

        List<int> decoys = new List<int>();
        for (int i = 0; i < clueNest.Count; i++)
        {
            if (clueNest[i] == result.nest) result.clues.Add(i);
            else if (clueNest[i] < 0) decoys.Add(i);
        }

        // Partial Fisher-Yates: the first n decoys end up random.
        int take = Math.Min(Math.Max(0, decoysToShow), decoys.Count);
        for (int i = 0; i < take; i++)
        {
            int j = rng.Next(i, decoys.Count);
            (decoys[i], decoys[j]) = (decoys[j], decoys[i]);
            result.clues.Add(decoys[i]);
        }

        result.clues.Sort();
        return result;
    }
}
