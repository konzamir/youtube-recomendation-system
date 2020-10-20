import Home from "@/pages/Home";
import Featured from "@/pages/Featured";
import VideoInfo from "@/pages/VideoInfo";


export default [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/featured/",
    name: "featured",
    component: Featured
  },
  {
    path: "/video/",
    name: "videoInfo",
    component: VideoInfo
  },
];
