import auth from './auth';
import filters from './filters';
import processes from './processes';
import videos from './videos';

export default {
    ...videos,
    ...auth,
    ...filters,
    ...processes
}