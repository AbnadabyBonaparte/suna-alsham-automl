/**
 * Type declarations for @react-three/fiber and @react-three/drei beta.
 * These override incomplete/broken types from the beta packages.
 */

/* eslint-disable @typescript-eslint/no-explicit-any */

declare module '@react-three/fiber' {
  export const Canvas: React.FC<any>;
  export function useFrame(callback: (state: any, delta: number) => void): void;
  export function useThree(): any;
}

declare module '@react-three/drei' {
  export const OrbitControls: React.FC<any>;
  export const Sphere: React.ForwardRefExoticComponent<any>;
  export const Points: React.ForwardRefExoticComponent<any>;
  export const PointMaterial: React.FC<any>;
  export const Line: React.FC<any>;
  export const Html: React.FC<any>;
  export const Text: React.FC<any>;
  export const Float: React.FC<any>;
  export const Stars: React.FC<any>;
}
