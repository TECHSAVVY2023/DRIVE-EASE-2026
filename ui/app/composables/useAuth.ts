/**
 * Thin auth composable — all logic lives in Central-API (Django).
 * The UI only stores the JWT returned by the API callback and calls
 * API endpoints for login / logout / user info.
 */

import { useApiBase } from '~/utils/api/api';

interface AuthUser {
    id: number | string;
    given_name?: string;
    family_name?: string;
    email?: string;
    picture?: string;
    contact_number?: string;
    address?: string;
    profile_picture?: string;
    license_image?: string;
    id_image?: string;
    date_joined?: string;
}

export const useAuth = () => {
    const user = useState<AuthUser | null>('auth_user', () => null);
    const token = useState<string | null>('auth_token', () => null);

    const isLoggedIn = computed(() => !!token.value);

    /**
     * Initialise auth state from localStorage (client-side only).
     */
    const init = (): void => {
        if (!import.meta.client) return;

        const storedToken = localStorage.getItem('auth_token');
        const storedUser = localStorage.getItem('auth_user');

        if (storedToken) token.value = storedToken;

        if (storedUser) {
        try {
            user.value = JSON.parse(storedUser) as AuthUser;
        } catch {
            user.value = null;
        }
        }
    };

    /**
     * Persist the JWT that the Django callback appends as ?token=…
     * and fetch the user profile from the API.
     */
    const setAuth = async (jwt: string): Promise<void> => {
        if (!import.meta.client) return;

        localStorage.setItem('auth_token', jwt);
        token.value = jwt;

        try {
        const apiBase = useApiBase();
        const profile = await $fetch<AuthUser>(`${apiBase}/api/driveease/auth/me/`, {
            headers: { Authorization: `Bearer ${jwt}` },
        });

        const userData: AuthUser = {
            id: profile.id,
            given_name: profile.given_name,
            family_name: profile.family_name,
            email: profile.email,
            picture: profile.picture,
            date_joined: profile.date_joined,
            contact_number: profile.contact_number,
            address: profile.address,
            profile_picture: profile.profile_picture,
            license_image: profile.license_image,
            id_image: profile.id_image,
        };

        localStorage.setItem('auth_user', JSON.stringify(userData));
        user.value = userData;
        console.log('User profile:', userData);
        
        } catch (err) {
            console.error('Failed to fetch user profile:', err);
        }
    };

    /**
     * Redirect to the Django Google OAuth endpoint.
     */
    const login = (): void => {
        if (!import.meta.client) return;
        const apiBase = useApiBase();
        const origin = window.location.origin;
        window.location.href = `${apiBase}/api/driveease/auth/google/?origin=${encodeURIComponent(origin)}`;
    };

    /**
     * Clear local auth state and redirect to the home page.
     */
    const logout = (): void => {
        if (import.meta.client) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        }

        token.value = null;
        user.value = null;

        navigateTo('/');
    };

    return {
        user,
        token,
        isLoggedIn,
        init,
        setAuth,
        login,
        logout,
    };
};
