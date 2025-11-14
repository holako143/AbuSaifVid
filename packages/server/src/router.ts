import { z } from 'zod';
import { authRouter } from './auth.router';
import { movieRouter } from './movie.router';
import { router, procedure } from './trpc';

export const appRouter = router({
  auth: authRouter,
  movie: movieRouter,
  hello: procedure
    .input(z.object({ text: z.string() }))
    .query(({ input }) => {
      return {
        greeting: `hello ${input.text}`,
      };
    }),
});

export type AppRouter = typeof appRouter;
