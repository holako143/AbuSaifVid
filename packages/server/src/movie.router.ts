import { prisma } from './db';
import { z } from 'zod';
import { router, procedure } from './trpc';

export const movieRouter = router({
  getMovies: procedure
    .query(async () => {
      return await prisma.movie.findMany({
        include: {
          links: true,
        },
      });
    }),

  addMovie: procedure
    .input(z.object({
      title: z.string(),
      description: z.string().optional(),
      links: z.array(z.object({
        url: z.string().url(),
        type: z.string(),
      })),
    }))
    .mutation(async ({ input }) => {
      const { title, description, links } = input;
      const movie = await prisma.movie.create({
        data: {
          title,
          description,
          links: {
            create: links,
          },
        },
        include: {
          links: true,
        },
      });
      return movie;
    }),
});
