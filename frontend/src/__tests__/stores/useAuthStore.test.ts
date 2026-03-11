import { useAuthStore } from '@/stores/useAuthStore';
import { act } from '@testing-library/react';

describe('useAuthStore', () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      session: null,
      metadata: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  });

  it('should have correct initial state', () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.session).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.metadata).toBeNull();
  });

  it('should set user and update isAuthenticated', () => {
    const mockUser = { id: 'test-123', email: 'test@test.com' } as any;
    
    act(() => {
      useAuthStore.getState().setUser(mockUser);
    });

    const state = useAuthStore.getState();
    expect(state.user).toEqual(mockUser);
    expect(state.isAuthenticated).toBe(true);
  });

  it('should logout and clear all state', () => {
    const mockUser = { id: 'test-123', email: 'test@test.com' } as any;
    
    act(() => {
      useAuthStore.getState().setUser(mockUser);
    });
    
    expect(useAuthStore.getState().isAuthenticated).toBe(true);
    
    act(() => {
      useAuthStore.setState({
        user: null,
        session: null,
        metadata: null,
        isAuthenticated: false,
      });
    });

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.session).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.metadata).toBeNull();
  });

  it('should set and clear error', () => {
    act(() => {
      useAuthStore.getState().setError('Test error');
    });
    expect(useAuthStore.getState().error).toBe('Test error');

    act(() => {
      useAuthStore.getState().setError(null);
    });
    expect(useAuthStore.getState().error).toBeNull();
  });

  it('should compute hasFounderAccess correctly', () => {
    const founderUser = { id: '1', email: 'casamondestore@gmail.com' } as any;
    
    act(() => {
      useAuthStore.getState().setUser(founderUser);
    });
    
    expect(useAuthStore.getState().hasFounderAccess()).toBe(true);
  });

  it('should compute hasFounderAccess as false for regular users', () => {
    const regularUser = { id: '1', email: 'regular@test.com' } as any;
    
    act(() => {
      useAuthStore.getState().setUser(regularUser);
    });
    
    expect(useAuthStore.getState().hasFounderAccess()).toBe(false);
  });

  it('should get userId and userEmail', () => {
    const mockUser = { id: 'uid-456', email: 'user@domain.com' } as any;
    
    act(() => {
      useAuthStore.getState().setUser(mockUser);
    });

    expect(useAuthStore.getState().getUserId()).toBe('uid-456');
    expect(useAuthStore.getState().getUserEmail()).toBe('user@domain.com');
  });

  it('should return null for userId/userEmail when no user', () => {
    expect(useAuthStore.getState().getUserId()).toBeNull();
    expect(useAuthStore.getState().getUserEmail()).toBeNull();
  });
});
