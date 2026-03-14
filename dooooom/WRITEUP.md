# DOOM — Friendly Fire: Companion Bot Submission

## What Was Built
I added a friendly companion bot that follows the player through the level and actively fights other enemies. I repurposed the Zombieman (`MT_POSSESSED`) to act as the companion by giving it a custom behavior flag. To keep the implementation native and consistent with the engine's design, no new behaviors were created from scratch; rather, the existing state machine and Thinker systems were slightly modified to invert targeting logic and prevent friendly fire.

## Codebase Modifications
The implementation required changes in four main files within `chocolate-doom/src/doom/`:

1. **`p_mobj.h`**:
   - Added a new flag `MF_FRIEND (0x10000000)` to the `mobjflag_t` enum. This flag acts as the identifier for companion entities, distinguishing them from standard enemies.

2. **`p_setup.c`**:
   - Created `P_SpawnCompanion()`, which spawns a `MT_POSSESSED` actor near the player's spawn coordinates (`player->x + 64 * FRACUNIT`).
   - Equipped the spawned actor with the `MF_FRIEND` flag, removed the `MF_COUNTKILL` flag so it isn't required for 100% kills, and bumped its health to `2000` to increase its survivability alongside the player.
   - Tied `P_SpawnCompanion()` into `P_SetupLevel()`, right after the player spawn initialization, guaranteeing the bot spawns at the beginning of maps.

3. **`p_enemy.c`**:
   - Modified `A_Look()`. Typically, `A_Look()` scans the environment for `MT_PLAYER`. If the thinker has the `MF_FRIEND` flag, it intercepts the regular call and redirects it to a new helper function `P_LookForMonsters()`.
   - Created `P_LookForMonsters()`, which iterates through `thinkercap` (the global list of active AI entities in the level). It skips non-shootables, the player, and other companions, then selects the closest valid hostile monster within line-of-sight (`P_CheckSight`). Once found, it updates the companion's `target` and sends it into its `seestate` (chasing/attacking).

4. **`p_inter.c`**:
   - Updated `P_DamageMobj()` to implement strict friendly fire rules. The added conditions ensure that a source with `MF_FRIEND` cannot damage `MT_PLAYER`, `MT_PLAYER` cannot damage a target with `MF_FRIEND`, and `MF_FRIEND` entities cannot damage each other.

## Known Challenges & Behavioral Edge Cases
- **Getting Stuck**: Sometimes the companion can block doorways or get stuck behind walls due to DOOM's original AI chasing logic, which isn't full pathfinding but zig-zagging towards the target. It primarily succeeds using `P_Move()`.
- **Friendly Fire & Infighting**: DOOM relies heavily on monster infighting. While the core friendly-fire patch prevents direct health deduction between the player and the companion, explosive splash damage (like rockets or barrels) required careful evaluation. Since `P_DamageMobj` acts as the root damage delegator, the early return perfectly shields the companion.

## Getting Started
The modified code is ready to compile! Build the project using `make` inside the `chocolate-doom` folder and run `./src/chocolate-doom -iwad freedoom1.wad` to jump in with your new teammate!
