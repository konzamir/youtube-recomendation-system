import Home from "@/pages/Home";
import Featured from "@/pages/Featured";
import VideoInfo from "@/pages/VideoInfo";
import NotFound from "@/pages/NotFound";

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
    path: "*",
    component: NotFound
  }
];
