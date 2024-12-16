import rclpy
from liorf.srv import SaveMap
from datetime import datetime

def send_request():
    # Initialize ROS 2
    rclpy.init()

    # Create a node
    node = rclpy.create_node('save_map_client')

    # Create a client for the SaveMap service
    client = node.create_client(SaveMap, 'liorf/save_map')

    # Wait for the service to become available
    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Waiting for SaveMap service to become available...')

    # Create a request
    request = SaveMap.Request()
    request.resolution = 0.05  # Example resolution
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    request.destination = '/unitec_code/maps/'+str(current_timestamp)  # Example file path

    # Call the service
    future = client.call_async(request)

    # Wait for the response
    rclpy.spin_until_future_complete(node, future)

    # Handle the response
    if future.result() is not None:
        if future.result().success:
            node.get_logger().info('Map saved successfully!')
        else:
            node.get_logger().info('Failed to save the map.')
    else:
        node.get_logger().error('Service call failed!')

    # Shut down ROS 2
    rclpy.shutdown()

if __name__ == '__main__':
    send_request()
