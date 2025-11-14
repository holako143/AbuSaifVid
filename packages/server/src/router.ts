import { initTRPC } from '@trpc/server';
import { z } from 'zod';
import { authRouter } from './auth.router';

const t = initTRPC.create();

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
