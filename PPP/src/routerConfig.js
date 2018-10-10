import Home from './pages/Home';
import Predict from './pages/Predict';
import NotFound from './pages/NotFound';

const routerConfig = [
  {
    path: '/',
    component: Home,
  },
  {
    path: '/predict/:data',
    component: Predict,
  },
  {
    path: '*',
    component: NotFound,
  },
];

export default routerConfig;
