import { t } from './trpc';
import { z } from 'zod';
import { authRouter } from './auth.router';

export const appRouter = t.router({
  auth: authRouter,
  hello: t.procedure
    .input(z.object({ text: z.string() }))
    .query(({ input }) => {
      return {
        greeting: `hello ${input.text}`,
      };
    }),
});

export type AppRouter = typeof appRouter;
