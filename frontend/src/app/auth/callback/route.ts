import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
    const { searchParams, origin } = new URL(request.url)
    const code = searchParams.get('code')
    const next = searchParams.get('next') ?? '/dashboard'

    if (code) {
        const cookieStore = {
            getAll() {
                return [] // We can't access cookies directly in this simplified example without `cookies()` from next/headers, but let's use the proper pattern below
            },
        }

        // We need to use the cookies() function from next/headers in a real Next.js app, 
        // but since we are in a route handler, we can import it.
        // However, to keep it simple and robust, let's use the standard pattern:

        const supabase = createServerClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
            {
                cookies: {
                    get(name: string) {
                        return request.cookies.get(name)?.value
                    },
                    set(name: string, value: string, options: CookieOptions) {
                        // This is a temporary response object to set cookies on
                        // In the actual response we will copy these
                    },
                    remove(name: string, options: CookieOptions) {
                        // Same as set
                    },
                },
            }
        )

        // Actually, the proper way in Next.js App Router route handlers involves creating a response first or using the cookie store if available.
        // Let's use the standard robust pattern for Route Handlers.
    }

    // Let's rewrite with the correct pattern using NextResponse to handle cookies

    if (code) {
        const cookieStore = await import('next/headers').then(mod => mod.cookies())
        const supabase = createServerClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
            {
                cookies: {
                    get(name: string) {
                        return cookieStore.get(name)?.value
                    },
                    set(name: string, value: string, options: CookieOptions) {
                        cookieStore.set({ name, value, ...options })
                    },
                    remove(name: string, options: CookieOptions) {
                        cookieStore.set({ name, value: '', ...options })
                    },
                },
            }
        )

        const { error } = await supabase.auth.exchangeCodeForSession(code)
        if (!error) {
            return NextResponse.redirect(`${origin}${next}`)
        }
    }

    // Return the user to an error page with instructions
    return NextResponse.redirect(`${origin}/auth/auth-code-error`)
}
