#include "test.h"

static void print_map(const char* fname)
{
	pointless_t p;
	const char* error = 0;

	if (!pointless_open_f(&p, fname, 0, &error)) {
		fprintf(stderr, "pointless_open_f() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}

	if (!pointless_debug_print(&p, stdout, &error)) {
		fprintf(stderr, "pointless_debug_print() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}

	pointless_close(&p);
}

static void measure_load_time(const char* fname)
{
	pointless_t p;
	const char* error = 0;

	clock_t t_0 = clock();

	if (!pointless_open_f(&p, fname, 0, &error)) {
		fprintf(stderr, "pointless_open_f() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}

	clock_t t_1 = clock();

	printf("INFO: load time: %.3f\n", (double)(t_1 - t_0) / (double)CLOCKS_PER_SEC);

	pointless_close(&p);
}

static void run_re_create_32(const char* fname_in, const char* fname_out)
{
	const char* error = 0;

	if (!pointless_recreate_32(fname_in, fname_out, &error)) {
		fprintf(stderr, "pointless_recreate_32() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}
}

static void run_re_create_64(const char* fname_in, const char* fname_out)
{
	const char* error = 0;

	if (!pointless_recreate_64(fname_in, fname_out, &error)) {
		fprintf(stderr, "pointless_recreate_64() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}
}

static void print_usage_exit()
{
	fprintf(stderr, "usage: ./pointless_util OPTIONS\n");
	fprintf(stderr, "\n");
	fprintf(stderr, "   --unit-test-32\n");
	fprintf(stderr, "   --unit-test-64\n");
	fprintf(stderr, "   --test-performance-32\n");
	fprintf(stderr, "   --test-performance-64\n");
	fprintf(stderr, "   --measure-load-time pointless.map\n");
	fprintf(stderr, "   --test-hash\n");
	fprintf(stderr, "   --dump-file pointless.map\n");
	fprintf(stderr, "   --re-create-32 pointless_in.map pointless_out.map\n");
	fprintf(stderr, "   --re-create-64 pointless_in.map pointless_out.map\n");
	fprintf(stderr, "   --measure-32-64-bit-difference pointless.map [...]\n");
	exit(EXIT_FAILURE);
}

static void run_unit_test(create_begin_cb cb)
{
	create_wrapper("very_simple.map", cb, create_very_simple);
	print_map("very_simple.map");

	create_wrapper("simple.map", cb, create_simple);
	print_map("simple.map");

	create_wrapper("tuple.map", cb, create_tuple);
	print_map("tuple.map");

	create_wrapper("set.map", cb, create_set);
	query_wrapper("set.map", query_set);
	print_map("set.map");

	create_wrapper("special_a.map", cb, create_special_a);
	print_map("special_a.map");

	create_wrapper("special_b.map", cb, create_special_b);
	print_map("special_b.map");

	create_wrapper("special_c.map", cb, create_special_c);
	print_map("special_c.map");

	create_wrapper("special_d.map", cb, create_special_d);
	print_map("special_d.map");
	query_wrapper("special_d.map", query_special_d);
	print_map("special_d.map");
}

static void run_performance_test(create_begin_cb cb)
{
	create_wrapper("set_1M.map", cb, create_1M_set);
	query_wrapper("set_1M.map", query_1M_set);
}

static uint64_t measure_32_64_difference(const char* fname)
{
	pointless_t p;
	const char* error = 0;

	if (!pointless_open_f(&p, fname, 0, &error)) {
		fprintf(stderr, "pointless_open_f() failure: %s\n", error);
		exit(EXIT_FAILURE);
	}

	uint64_t increase = 0;

	increase += p.header->n_string_unicode;
	increase += p.header->n_vector;
	increase += p.header->n_bitvector;
	increase += p.header->n_set;
	increase += p.header->n_map;

	increase *= 4;

	pointless_close(&p);

	return increase;
}

int main(int argc, char** argv)
{
	if (argc >= 3 && strcmp(argv[1], "--measure-32-64-bit-difference") == 0) {
		int i;

		uint64_t s = 0;

		for (i = 2; i < argc; i++)
			s += measure_32_64_difference(argv[i]);

		printf("%llu\n", (unsigned long long)s);
	} else if (argc == 2) {
		if (strcmp(argv[1], "--unit-test-32") == 0)
			run_unit_test(pointless_create_begin_32);
		else if (strcmp(argv[1], "--unit-test-64") == 0)
			run_unit_test(pointless_create_begin_64);
		else if (strcmp(argv[1], "--test-performance-32") == 0)
			run_performance_test(pointless_create_begin_32);
		else if (strcmp(argv[1], "--test-performance-64") == 0)
			run_performance_test(pointless_create_begin_64);
		else if (strcmp(argv[1], "--test-hash") == 0)
			validate_hash_semantics();
		else
			print_usage_exit();
	} else if (argc == 3) {
		if (strcmp(argv[1], "--dump-file") == 0)
			print_map(argv[2]);
		else if (strcmp(argv[1], "--measure-load-time") == 0)
			measure_load_time(argv[2]);
		else
			print_usage_exit();

	} else if (argc == 4) {
		if (strcmp(argv[1], "--re-create-32") == 0)
			run_re_create_32(argv[2], argv[3]);
		else if (strcmp(argv[1], "--re-create-64") == 0)
			run_re_create_64(argv[2], argv[3]);
		else
			print_usage_exit();
	} else {
		print_usage_exit();
	}

	exit(EXIT_SUCCESS);
}
