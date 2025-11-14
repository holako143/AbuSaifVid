import { prisma } from './db';

export const createContext = () => ({
  prisma,
});
