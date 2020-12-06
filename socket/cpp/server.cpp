#include <arpa/inet.h>
#include <fcntl.h>
#include <netdb.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cstdio>
#include <cstring>
#include <iostream>
#include <set>
#include <vector>

#define EPOLLSIZE 65536
#define LISTEN_QUEUE SOMAXCONN

#define DEBUG

#ifdef DEBUG
#define debug(...)                            \
    std::cerr << "LINE " << __LINE__ << ": "; \
    _dbg(#__VA_ARGS__, __VA_ARGS__)
#else
#define debug(...)
#endif

template <typename T>
void _dbg(const char* sdbg, T h) {
    std::cerr << sdbg << '=' << h << std::endl;
}
template <typename T, typename... Aargs>
void _dbg(const char* sdbg, T h, Aargs... a) {
    while (*sdbg != ',') std::cerr << *sdbg++;
    std::cerr << '=' << h << ',';
    _dbg(sdbg + 1, a...);
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& v) {
    os << "[";
    for (auto& x : v) {
        os << x << ",";
    }
    return os << "]";
}

template <typename L, typename R>
std::ostream& operator<<(std::ostream& os, const std::pair<L, R>& p) {
    return os << "(" << p.first << "," << p.second << ")";
}

using namespace std;

int update_fcntl_flag(int fd) {
    int flag = fcntl64(fd, F_GETFL, 0);
    if (flag == -1) {
        perror("fcntl64 F_GETFL");
        return -1;
    }

    flag |= O_NONBLOCK | O_CLOEXEC;
    if (fcntl64(fd, F_SETFL, flag) != 0) {
        char* message = new char[50];
        if (sprintf(message, "fcntl64 F_SETFL %#x", flag) < 0) {
            perror("fcntl64 F_SETFL -> sprintf");
        } else {
            perror(message);
        }
        delete message;
        return -1;
    }

    return 0;
}

int listen_port(const char* address, const char* port, set<int>* results) {
    addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;

    addrinfo* addrs;
    int ret = getaddrinfo(address, port, &hints, &addrs);
    if (ret != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(ret));
        return -1;
    }

    for (addrinfo* p = addrs; p != nullptr; p = p->ai_next) {
        int fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (fd != 0) {
            perror("socket");
            continue;
        }

        if (update_fcntl_flag(fd) != 0) {
            if (close(fd) != 0) {
                perror("close");
            }
            continue;
        }

        if (bind(fd, p->ai_addr, p->ai_addrlen) != 0) {
            perror("bind");
            if (close(fd) != 0) {
                perror("close");
            }
            continue;
        }

        if (listen(fd, LISTEN_QUEUE) != 0) {
            perror("listen");
            if (close(fd) != 0) {
                perror("close");
                continue;
            }
        }

        results->insert(fd);
    }

    freeaddrinfo(addrs);
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <port>", argv[0]);
        return -1;
    }

    int epfd = epoll_create1(EPOLL_CLOEXEC);

    set<int> fds;
    if (listen_port(nullptr, argv[1], &fds) != 0) {
        return -1;
    }

    if (fds.size() == 0) {
        fprintf(stderr, "Unable to bind any port");
        return -1;
    }
    return 0;
}