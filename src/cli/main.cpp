#include <string>
#include "mana_client.hpp"



int main(int argc, char** argv) {
	ManaClient client {};
	std::string obj;
	std::string operation;
	std::string arg;

	if (argc > 1) {
		obj = argv[1];
	}

	if (argc > 2) {
		operation = argv[2];
	}

	if (argc > 3) {
		arg = argv[3];
	}

	client.new_project("test");
	return 0;
}
