# Web 3D Integration Patterns - Skill Summary

This meta-skill synthesizes architectural approaches for combining Three.js, GSAP ScrollTrigger, React Three Fiber, Motion, and React Spring into cohesive 3D web applications.

## Core Architecture Patterns

**Pattern 1: Layered Separation** organizes code into distinct 3D (Three.js), animation (GSAP), and UI (React) layers. This approach suits scroll-driven experiences with overlaid interfaces, offering clear separation of concerns but requiring manual synchronization between layers.

**Pattern 2: Unified React Components** leverages React Three Fiber with declarative animation libraries like Motion. This React-first strategy provides unified state management and component reusability, though it demands learning R3F's paradigms.

**Pattern 3: Hybrid Approach** combines R3F with GSAP timelines for complex animation sequences while maintaining React state management—balancing control and declarativity.

**Pattern 4: Physics-Based 3D** uses R3F with React Spring to create natural, physics-driven interactions with "wobbly" or "smooth" spring configurations.

## Critical Integration Challenges

Animation conflicts arise when multiple libraries target the same property. Solution: assign one library per property or coordinate timing precisely.

State synchronization requires either refs or state management solutions (Zustand recommended). Without synchronization, Three.js updates won't reflect in React state.

Memory leaks occur from unearthed animations. Always kill GSAP tweens and clear listeners in `useEffect` cleanup functions.

## Performance Optimization

Coordinate render loops across libraries—use "demand" frameloop in R3F to render only when necessary. Implement conditional rendering based on interaction detection.

For Three.js + GSAP integration, manually trigger re-renders via interaction callbacks rather than continuous polling.

## Decision Framework

- **Scroll-driven marquee experiences**: Three.js + GSAP dominates this space
- **Interactive product viewers**: R3F + Motion offers rapid development
- **Timeline-based sequences**: R3F + GSAP combines component declarativity with GSAP's timeline strength
- **Gesture-driven physics**: R3F + React Spring feels most natural

The skill emphasizes referencing foundation skills (threejs-webgl, gsap-scrolltrigger, react-three-fiber, etc.) for library-specific API details while using this meta-skill for architectural decisions and integration strategy.
