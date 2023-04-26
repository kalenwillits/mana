#include "mana_client.hpp"
#include "HTTPRequest.hpp"
#include <chrono>
#include <unistd.h>


ManaClient::ManaClient() : 
	base_url{"http://localhost:8000/"},
	protocol{http::InternetProtocol::v4}
{
}

void ManaClient::new_project(const std::string name) {
	http::Request request {base_url + "project/new/", protocol};
	const auto response = request.send(
			"POST", 
			"{\"name\":\"test201\"}",
			{
				{"Content-Type", "application/json"},
				{"Accept", "*/*"},
				{"username", "kalen"},
				{"password", "pass"}
			}
		);

	switch (response.status.code) {
		case http::Status::Ok:
			std::cout << "OK" << std::endl;
			break;
		case http::Status::Created:
			std::cout << "Created" << std::endl;
			break;
		case http::Status::Accepted:
			std::cout << "Accepted" << std::endl;
			break;
		case http::Status::Conflict:
			std::cout << "Conflict" << std::endl;
			break;
		case http::Status::BadRequest:
			std::cout << "BadRequest" << std::endl;
			break;
		default:
			std::cout << "Something else happened..." << std::endl;
	}


	std::cout << std::string{response.body.begin(), response.body.end()} << std::endl;
}

