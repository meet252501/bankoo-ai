# BANKOO AI - GRANDMASTER LOGIC CORE (GOD MODE EDITION)
# This file contains the "Deep Logic" for every supported language.
# It acts as a context injection layer to ensure the AI uses the correct libraries, idioms, and architecture.
# "SHORTCUTS TO 100" requested: Now includes GLOBAL PROTOCOLS and HALLUCINATION GUARDS.

LANGUAGE_LOGIC = {
    # 0. GLOBAL PROTOCOLS (Injected before specific logic)
    "__GLOBAL__": (
        "GLOBAL GRANDMASTER PROTOCOLS:\n"
        "- HALLUCINATION GUARD: NEVER use libraries that do not exist (e.g., 'std::json' for C++, 'async_os' for Python). Check Std Lib docs mentally.\n"
        "- ARCHITECTURE: Prefer COMPOSITION over INHERITANCE. Use HEXAGONAL ARCHITECTURE for business logic.\n"
        "- HARDWARE ALIGNMENT: Prefer STACK allocation for small objects, HEAP only for dynamic/large data. Use ZERO-COPY where possible.\n"
        "- DETERMINISM: No random behavior unless requested. Seed all PRNGs.\n"
    ),

    # 1. PYTHON
    "python": (
        "DEEP LOGIC [PYTHON 3.12+]:\n"
        "- FRAMEWORK SHORTCUT: Web? Use `FastAPI`. Data? Use `Polars` (faster than Pandas) or `numpy`.\n"
        "- HALLUCINATION GUARD: NO `std::json`. NO `requests` (if std-lib only). NO `async_file` (use `pathlib`).\n"
        "- ARCHITECTURE: Use `Dependency Injection` for services. Typed Dicts for config.\n"
        "- GRANDMASTER REFERENCE (Metaclass):\n"
        "   ```python\n"
        "   class Meta(type): def __new__(mcs, name, bases, attrs): return super().__new__(mcs, name, bases, attrs)\n"
        "   ```\n"
    ),

    # 2. RUST
    "rust": (
        "DEEP LOGIC [RUST 2021]:\n"
        "- FRAMEWORK SHORTCUT: Web? `Axum`. Serialization? `Serde`.\n"
        "- HALLUCINATION GUARD: NO `std::json`. NO `tokio` (if std-lib only). NO `std::rand` (it is an external crate `rand`).\n"
        "- MEMORY: Use `Cow<'a, str>` to minimize allocations. Use `SmallVec` logic.\n"
        "- GRANDMASTER REFERENCE (Generic Trait):\n"
        "   ```rust\n"
        "   trait Transform<T> { fn transform(&self) -> T; }\n"
        "   ```\n"
    ),

    # 3. C++
    "c++": (
        "DEEP LOGIC [C++20]:\n"
        "- FRAMEWORK SHORTCUT: JSON? `nlohmann`. Web? `Crow` or `Drogon`.\n"
        "- HALLUCINATION GUARD: NO `std::json`. NO `std::thread_pool` (not in std lib). NO `magic_enum` (external).\n"
        "- HARDWARE: Enforce `Data Oriented Design` (DOD). Use SoA (Structure of Arrays) for cache friendliness.\n"
        "- GRANDMASTER REFERENCE (CRTP):\n"
        "   ```cpp\n"
        "   template <typename T> class Base { void interface() { static_cast<T*>(this)->impl(); } };\n"
        "   ```\n"
    ),

    # 4. GO (Golang)
    "go": (
        "DEEP LOGIC [GO 1.22+]:\n"
        "- FRAMEWORK SHORTCUT: Router? `chi`. CLI? `cobra`.\n"
        "- HALLUCINATION GUARD: NO `std/json` (it is `encoding/json`). NO `context.Base` (use `context.Background`).\n"
        "- ARCHITECTURE: 'Return values, accept interfaces'. 100% test coverage via Table Tests.\n"
        "- GRANDMASTER REFERENCE (Select/Timeout):\n"
        "   ```go\n"
        "   select { case res := <-c: return res; case <-time.After(1 * time.Second): return err }\n"
        "   ```\n"
    ),

    # 5. JAVA
    "java": (
        "DEEP LOGIC [JAVA 21]:\n"
        "- FRAMEWORK SHORTCUT: Cloud? `Micronaut`. CLI? `Picocli`.\n"
        "- HALLUCINATION GUARD: NO `java.util.JSON`. NO `javax.servlet` (if using Spring Boot/Jakarta).\n"
        "- MEMORY: Use `Virtual Threads` (Loom) for high throughput. Avoid GC-heavy allocations in tight loops.\n"
        "- GRANDMASTER REFERENCE (Sealed Class):\n"
        "   ```java\n"
        "   public sealed interface Shape permits Circle, Square {}\n"
        "   ```\n"
    ),

    # 6. JAVASCRIPT (Node.js)
    "javascript": (
        "DEEP LOGIC [NODE 20+]:\n"
        "- FRAMEWORK SHORTCUT: Backend? `Fastify` (faster than Express). Testing? `node:test` (built-in).\n"
        "- HALLUCINATION GUARD: NO `fs.promises.exists` (deprecated, use `access`). NO `import.meta.url` in CJS.\n"
        "- ARCHITECTURE: Use `ESM` by default. Use `Worker Threads` for heavy logic.\n"
        "- GRANDMASTER REFERENCE (Proxy Object):\n"
        "   ```javascript\n"
        "   const p = new Proxy(obj, { get: (t, k) => k in t ? t[k] : 42 });\n"
        "   ```\n"
    ),

    # 7. TYPESCRIPT
    "typescript": (
        "DEEP LOGIC [TS 5.0+]:\n"
        "- FRAMEWORK SHORTCUT: Validation? `Zod`. Type safety? `tRPC`.\n"
        "- HALLUCINATION GUARD: NO `Type.Array`. NO `Array.of<T>`. Use `T[]`.\n"
        "- TYPE SYSTEM: Use `Branded Types` (Opaque Types) for ID safety (`UserId = string & { __brand: 'User' }`).\n"
        "- GRANDMASTER REFERENCE (Satisfies):\n"
        "   ```typescript\n"
        "   const theme = { color: 'red' } satisfies Record<string, string>;\n"
        "   ```\n"
    ),

    # 8. PHP
    "php": (
        "DEEP LOGIC [PHP 8.3]:\n"
        "- HALLUCINATION GUARD: NO `std::array`. NO `$_POST['key']` without `filter_input`.\n"
        "- ARCHITECTURE: Use `Attribute` for metadata. Final classes by default.\n"
        "- GRANDMASTER REFERENCE (Readonly):\n"
        "   ```php\n"
        "   readonly class User { public function __construct(public string $name) {} }\n"
        "   ```\n"
    ),

    # 9. RUBY
    "ruby": (
        "DEEP LOGIC [RUBY 3.3]:\n"
        "- HALLUCINATION GUARD: NO `std.json`. NO `Array.map!` (if frozen).\n"
        "- ARCHITECTURE: Use `Data.define` for simple immutable objects (Ruby 3.2+).\n"
        "- GRANDMASTER REFERENCE (Enumerator):\n"
        "   ```ruby\n"
        "   enum = Enumerator.new { |y| loop { y << 1 } }\n"
        "   ```\n"
    ),

    # 10. C#
    "c#": (
        "DEEP LOGIC [.NET 8]:\n"
        "- HALLUCINATION GUARD: NO `std.Console`. NO `var list = new List<string>()` (Use `List<string> list = [];`).\n"
        "- PERFORMANCE: Use `Primary Constructors`. Use `SearchValues<T>` for fast lookups.\n"
        "- GRANDMASTER REFERENCE (Interceptors):\n"
        "   ```csharp\n"
        "   [InterceptsLocation(\"file\", 1, 1)] public static void Map() { ... }\n"
        "   ```\n"
    ),

    # 11. C
    "c": (
        "DEEP LOGIC [STRICT C11]:\n"
        "- HALLUCINATION GUARD: NO `bool` without `<stdbool.h>`. NO `size_t` without `<stddef.h>`.\n"
        "- MEMORY: Use `Alignment` macros. Use `Static Analysis` hints (`_Nonnull`).\n"
        "- GRANDMASTER REFERENCE (Generic Selection):\n"
        "   ```c\n"
        "   #define type_name(x) _Generic((x), int: \"int\", float: \"float\", default: \"other\")\n"
        "   ```\n"
    ),

    # 12. SQL
    "sql": (
        "DEEP LOGIC [SQLITE/POSTGRES]:\n"
        "- HALLUCINATION GUARD: NO `FOR EACH LOOP`. NO `IF/ELSE` (Use `CASE`). NO `PRINT`.\n"
        "- PERFORMANCE: Use `EXPLAIN QUERY PLAN`. Avoid `N+1` in logical design.\n"
        "- GRANDMASTER REFERENCE (Window Filter):\n"
        "   ```sql\n"
        "   SELECT val, SUM(val) FILTER (WHERE val > 0) OVER() FROM data;\n"
        "   ```\n"
    ),

    # 13. BASH
    "bash": (
        "DEEP LOGIC [STRICT BASH]:\n"
        "- HALLUCINATION GUARD: NO `std.echo`. NO `file.exists()`. Use `[[ -f $f ]]`.\n"
        "- ARCHITECTURE: Use `local` variables only. Use `readonly` for constants.\n"
        "- GRANDMASTER REFERENCE (Indirect Ref):\n"
        "   ```bash\n"
        "   ref=\"var\"; echo \"${!ref}\"\n"
        "   ```\n"
    )
}
