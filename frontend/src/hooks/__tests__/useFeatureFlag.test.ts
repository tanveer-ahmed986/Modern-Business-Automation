/**
 * Tests for useFeatureFlag hook
 */

import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useFeatureFlag, useFeatureFlags, useHasAllFeatures, useHasAnyFeature } from '../useFeatureFlag';
import * as useSettingsModule from '../useSettings';

// Mock useSettings
vi.mock('../useSettings', () => ({
  useSettings: vi.fn(),
}));

describe('useFeatureFlag', () => {
  it('returns true when feature is enabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
          billing: true,
          ai_assistant: false,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlag('inventory'));

    expect(result.current).toBe(true);
  });

  it('returns false when feature is disabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
          billing: true,
          ai_assistant: false,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlag('ai_assistant'));

    expect(result.current).toBe(false);
  });

  it('returns false when settings are loading', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: null,
      isLoading: true,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlag('inventory'));

    expect(result.current).toBe(false);
  });

  it('returns false for non-existent feature', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlag('nonexistent_feature'));

    expect(result.current).toBe(false);
  });
});

describe('useFeatureFlags', () => {
  it('returns all feature flags', () => {
    const mockFlags = {
      inventory: true,
      billing: true,
      ai_assistant: false,
    };

    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: mockFlags,
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlags());

    expect(result.current).toEqual(mockFlags);
  });

  it('returns empty object when loading', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: null,
      isLoading: true,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useFeatureFlags());

    expect(result.current).toEqual({});
  });
});

describe('useHasAllFeatures', () => {
  it('returns true when all features are enabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
          billing: true,
          suppliers: true,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useHasAllFeatures(['inventory', 'billing']));

    expect(result.current).toBe(true);
  });

  it('returns false when any feature is disabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
          billing: false,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useHasAllFeatures(['inventory', 'billing']));

    expect(result.current).toBe(false);
  });
});

describe('useHasAnyFeature', () => {
  it('returns true when at least one feature is enabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: true,
          ai_assistant: false,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useHasAnyFeature(['inventory', 'ai_assistant']));

    expect(result.current).toBe(true);
  });

  it('returns false when all features are disabled', () => {
    vi.spyOn(useSettingsModule, 'useSettings').mockReturnValue({
      settings: {
        id: 1,
        business_name: 'Test Store',
        currency: 'USD',
        tax_rate: 15,
        feature_flags: {
          inventory: false,
          ai_assistant: false,
        },
      },
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    });

    const { result } = renderHook(() => useHasAnyFeature(['inventory', 'ai_assistant']));

    expect(result.current).toBe(false);
  });
});
