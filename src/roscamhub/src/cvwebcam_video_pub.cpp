#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sstream> // for converting the command line parameter to integer
#include <memory>
#include <rosutils/test.h>
#include "rosutils/batterymsg.h"


int main(int argc, char** argv)
{
  pp123(33);
  // rosutils::batterymsg battery;
  // battery.shuntvoltage = 0;
  // battery.busvoltage = 0;
  // battery.current_mA = 0;
  // battery.loadvoltage = 0;
  // battery.power_mW = 0;
  
  // Check if video source has been passed as a parameter
  if(argv[1] == NULL) return 1;

  ros::init(argc, argv, "image_publisher");
  ros::NodeHandle nh(argv[1]);
  nh.setParam("camfreq", 1);


  image_transport::ImageTransport it(nh);
  image_transport::Publisher pub = it.advertise("camera/image", 1);

  // Convert the passed as command line parameter index for the video device to an integer
  std::istringstream video_sourceCmd(argv[2]);
  int video_source;
  // Check if it is indeed a number
  if(!(video_sourceCmd >> video_source)) return 1;

  cv::VideoCapture cap(video_source);
  // Check if video device can be opened with the given index
  if(!cap.isOpened()) return 1;
  cv::Mat frame;
  sensor_msgs::ImagePtr msg;

  std::unique_ptr<ros::Rate> loop_rate_ptr( new ros::Rate(1) );

  int cnt = 0;
  int camfreq=1,prevcamfreq=1;
  while (nh.ok()) {
    ROS_INFO("send cv image" );

    cap >> frame;
    // Check if grabbed frame is actually full with some content
    if(!frame.empty()) {
      msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", frame).toImageMsg();
      pub.publish(msg);
      cv::waitKey(1);
    }

    ros::spinOnce();
    loop_rate_ptr->sleep();

    nh.getParam("camfreq", camfreq);
    
    if (camfreq!=prevcamfreq){
      loop_rate_ptr.reset(new ros::Rate(camfreq));
      prevcamfreq = camfreq;
    }

    ++cnt;

  }
}