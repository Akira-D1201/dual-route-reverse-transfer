# Dual-Route Reverse Transfer Model

A computational model comparing two cognitive routes of L3-to-L1 reverse transfer during Japanese cognate learning.

## Research Question

How does L1 Chinese word activation decline over 6 months of L3 Japanese learning, and does the decline pattern differ between orthographic (BIA+) and conceptual (non-selective) activation routes?

## Models

- **Model A (Orthographic)** : Simulates seeing a written cognate (e.g., 大学). Visual input activates only L1 and L3 nodes (shared orthography). L2 receives negligible activation. Based on the BIA+ framework (Dijkstra & Van Heuven, 2002).
- **Model B (Conceptual)** : Simulates seeing a picture. Conceptual input activates L1, L2, and L3 nodes simultaneously (non-selective activation). All languages compete for selection. Based on lexical competition models (Levelt, Roelofs & Meyer, 1999).

## Key Findings

1. Both routes show a **plateau phase** (Month 0-1) where L1 activation remains stable at baseline (0.80).
2. Both routes show an **inhibition breakout phase** (Month 1-3) where L1 activation drops sharply from 0.80 to ~0.09.
3. The conceptual route (Model B) shows slightly stronger suppression of L1, reflecting the additional competition from L2.
4. L2 (English) is also progressively suppressed by L3 in the conceptual route, as shown by the green dashed line.
5. Reverse transfer follows a **tipping-point dynamic** rather than a gradual linear trend.

## Implications

The model predicts that reverse transfer effects may be stronger in picture-naming tasks than in lexical decision tasks. Future empirical studies should compare these two task modalities to test this prediction, with particular attention to L2's mediating role in the conceptual route.

## File Structure

- `dual_route_reverse_transfer_model.py`: Python implementation of both models.
- `dual_route_comparison.png`: Visualization comparing L1 and L2 activation trajectories.

## Author

Wenjing DUAN

## License

This project is shared for academic portfolio purposes. If you use or adapt this code or ideas, please cite this repository.
