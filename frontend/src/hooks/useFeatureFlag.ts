/**
 * React hook for checking if a feature is enabled based on license tier.
 */

import { useSettings } from './useSettings';

export function useFeatureFlag(featureName: string): boolean {
  const { settings, isLoading } = useSettings();

  if (isLoading || !settings) {
    return false;
  }

  return settings.feature_flags?.[featureName] ?? false;
}

export function useFeatureFlags(): Record<string, boolean> {
  const { settings, isLoading } = useSettings();

  if (isLoading || !settings) {
    return {};
  }

  return settings.feature_flags ?? {};
}

/**
 * Check multiple features at once
 */
export function useHasAllFeatures(featureNames: string[]): boolean {
  const flags = useFeatureFlags();
  return featureNames.every(feature => flags[feature] === true);
}

/**
 * Check if at least one feature is enabled
 */
export function useHasAnyFeature(featureNames: string[]): boolean {
  const flags = useFeatureFlags();
  return featureNames.some(feature => flags[feature] === true);
}
