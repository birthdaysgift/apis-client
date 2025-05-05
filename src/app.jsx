import {
  useEffect,
  useState,
} from 'preact/hooks'
import {
  buildSchema,
  getIntrospectionQuery,
  graphql,
  isObjectType,
} from 'graphql'

function parseSDL(sdl) {
  const schema = buildSchema(sdl);

  const typeMap = schema.getTypeMap();

  let result = {};

  for (const typeName in typeMap) {
    const type = typeMap[typeName];
    if (isObjectType(type) && !typeName.startsWith('__')) {
      result["Type"] =
      console.log(`Type: ${type.name}`);
      const fields = type.getFields();
      for (const fieldName in fields) {
        const field = fields[fieldName];
        console.log(`  Field: ${fieldName}`);
        console.log(`    Type: ${field.type}`);
        if (field.args.length > 0) {
          console.log(`    Args:`);
          field.args.forEach(arg => {
            console.log(`      ${arg.name}: ${arg.type}`);
          });
        }
      }
    }
  }
}

export function App() {
  const [schemaJson, setSchemaJson] = useState(null);

  useEffect(() => {
    const runIntrospection = async () => {
      const sdl = `
        type Query {
          hello(name: String): String
          user(id: ID!): User
        }

        type User {
          id: ID!
          name: String
          age: Int
        }
      `;

      const schema = buildSchema(sdl);
      const result = await graphql({
        schema,
        source: getIntrospectionQuery(),
      });

      if (!result.errors) {
        setSchemaJson(result.data); // update state with JSON
        window.__schemaJson = result.data; // attach to window for debugging
      } else {
        console.error('Introspection errors:', result.errors);
      }
    };

    runIntrospection();
  }, []);

  return (
    <pre>{schemaJson ? JSON.stringify(schemaJson, null, 2) : 'Loading schema...'}</pre>
  )
}
