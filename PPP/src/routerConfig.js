import Home from './pages/Home';
import NotFound from './pages/NotFound';

const routerConfig = [
  {
    path: '/',
    component: Home,
  },
  {
    path: '*',
    component: NotFound,
  },
];

export default routerConfig;
