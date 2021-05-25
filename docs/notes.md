# Anathema Notes

## Application Structure

The application starts in the following way.

1. run.py -> calls to `anathema.main.main()`.
2. `anathema.main.main()`
   a. Configures the log
   b. Runs the `init()` method of `anathema.prepare` (currently does nothing)
        - This will eventually load the ECS, Components and Prefabs
        - We'll also load up the Console and any game assets
   c. Initializes `anathema.client.Client`.
   d. Runs `anathema.client.Client.main()`
3. `anathema.client.client.main()` will be the main game loop