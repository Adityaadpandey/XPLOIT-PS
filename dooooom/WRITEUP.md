# DOOM — Friendly Fire: Companion Bot Solution

## Overview
The goal of this challenge was to add a friendly companion bot that follows the player and fights enemies, utilizing the existing systems in DOOM without writing a completely new AI from scratch.

We achieved this by repurposing the Zombieman (`MT_POSSESSED`) into a companion. By using the existing Thinker state machines and collision code, we successfully allowed the bot to follow the player, engage in combat, and avoid inflicting or taking friendly fire.

---

## Codebase Modifications

All changes were made inside `chocolate-doom/src/doom/`:

### 1. `p_mobj.h` - Defining the Friend Flag
Added a new flag to the `mobjflag_t` enum to distinguish the companion from normal enemies.
```c
    // Friendly to player
    MF_FRIEND       = 0x10000000
```

### 2. `p_setup.c` - Spawning the Companion
Created `P_SpawnCompanion()` and added a call to it at the end of `P_SetupLevel()`. This ensures the bot spawns exactly when the player enters the map.
```c
void P_SpawnCompanion(void) {
    mobj_t* player = players[consoleplayer].mo;
    mobj_t* companion;

    // Spawn a marine-type companion near player
    companion = P_SpawnMobj(
        player->x + 64 * FRACUNIT,
        player->y,
        player->z,
        MT_POSSESSED
    );

    // Make it friendly, don't count towards kills, boost health
    companion->flags |= MF_FRIEND;
    companion->flags &= ~MF_COUNTKILL;
    companion->target = NULL;
    companion->health = 2000;
}
```

### 3. `p_enemy.c` - Companion Targeting Logic
Modified `A_Look()` to intercept typical enemy targeting. If the `MF_FRIEND` flag is present, it uses a custom helper function `P_LookForMonsters()` instead of looking for the player.
```c
void A_Look(mobj_t* actor) {
    // ...
    // If this is a companion, don't target player
    if (actor->flags & MF_FRIEND) {
        P_LookForMonsters(actor);
        return;
    }
    // ...
}
```
`P_LookForMonsters()` iterates through the `thinkercap` list to find the closest valid monster (that is shootable, alive, not the player, and not another friend) within line-of-sight (`P_CheckSight`), then assigns `actor->target` and changes the bot to its `seestate` to engage.

### 4. `p_inter.c` - Preventing Friendly Fire
Modified `P_DamageMobj()` to ensure mutual safety between the player and the companion, including protection against splash damage.
```c
    // Prevent friendly fire
    if (source && target) {
        if ((source->flags & MF_FRIEND) && target->type == MT_PLAYER) return;
        if (source->type == MT_PLAYER && (target->flags & MF_FRIEND)) return;
        if ((source->flags & MF_FRIEND) && (target->flags & MF_FRIEND)) return;
    }
```

---

## Steps to Recreate and Build

Since modern macOS environments (ARM64) require specific dependencies and architecture configurations to build legacy C code natively, using Docker is the cleanest way to compile the modified engine.

### Prerequisites
- Docker installed and running
- The `freedoom1.wad` file must be inside the `chocolate-doom` folder.

### Step 1: Compilation via Docker
Run the following set of commands from the root directory (`dooooom/`) to compile the game using an `amd64` Ubuntu container:

```bash
docker run --rm -v $(pwd):/work -w /work ubuntu:latest bash -c "\
apt-get update && \
apt-get install -y build-essential autoconf automake libtool pkg-config libsdl2-dev libsdl2-net-dev libsdl2-mixer-dev python3 libsamplerate0-dev && \
cd chocolate-doom && \
./autogen.sh && \
./configure && \
make -j4"
```

### Step 2: Running the Game
After the compilation is successful, you will have a `chocolate-doom` binary in `chocolate-doom/src/`.

**If you are on Linux or have X11 forwarding configured on macOS:**
```bash
cd chocolate-doom
./src/chocolate-doom -iwad freedoom1.wad
```

You can now start a new game, and the Zombieman companion will spawn right next to you and help you fight enemies across the map!
