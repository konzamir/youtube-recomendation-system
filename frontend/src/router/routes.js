import Home from "@/pages/Home";
import Featured from "@/pages/Featured";
import VideoInfo from "@/pages/VideoInfo";
import NotFound from "@/pages/NotFound";
import FailedYouTubeAuth from "@/pages/FailedYouTubeAuth";
import SuccessYouTubeAuth from "@/pages/SuccessYouTubeAuth";

export default [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/featured",
    name: "featured",
    component: Featured
  },
  {
    path: "/videos/:id",
    name: "videoInfo",
    component: VideoInfo
  },
  {
    path: "/successYouTubeAuth",
    component: SuccessYouTubeAuth
  },
  {
    path: "/failedYouTubeAuth",
    component: FailedYouTubeAuth
  },
  {
    path: "*",
    component: NotFound
  }
];
