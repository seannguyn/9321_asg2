import Home from './pages/Home';
import PredictPrice from './pages/PredictPrice';
import SuggestSuburb from './pages/SuggestSuburb';
import NotFound from './pages/NotFound';

const routerConfig = [
  {
    path: '/',
    component: Home,
  },
  {
    path: '/predict',
    component: PredictPrice,
  },
  {
    path: '/suggest',
    component: SuggestSuburb,
  },
  {
    path: '*',
    component: NotFound,
  },
];

export default routerConfig;
