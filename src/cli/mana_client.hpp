#ifndef MANA_CLIENT_HPP
#define MANA_CLIENT_HPP

#include <string>
#include <iostream>
#include "HTTPRequest.hpp"



class ManaClient {
	private:
		std::string base_url;
		http::InternetProtocol protocol;

	public:
		ManaClient();
		void new_project(const std::string name);
};

#endif
