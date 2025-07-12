# Project Knowledge Base
_Consolidated long-term memory - patterns, decisions, and learnings_

## Architecture & Design Decisions
<!-- Architectural decisions and their rationale -->

## Coding Standards & Conventions
<!-- Established patterns and naming conventions -->

## Domain Knowledge
<!-- Business rules, terminology, and workflows -->

## Recurring Patterns
<!-- Code patterns that appear 3+ times -->

## API Contracts
<!-- Endpoint definitions and data schemas -->

## Technical Learnings
<!-- Important discoveries and solutions -->

## 2025-07-12 22:09:47

# Project Knowledge Base - Adapta Hackathon Agent Backend
_Consolidated long-term memory - patterns, decisions, and learnings_

## Architecture & Design Decisions

### 🏗️ CORE ARCHITECTURE
- **Framework**: Backstage.io (Developer Portal Platform)
- **Language**: TypeScript for type safety
- **Architecture Pattern**: Clean Architecture with layers
- **API Strategy**: API-first development approach

### 🔧 TECHNOLOGY STACK
- **Runtime**: Node.js
- **Framework**: Backstage.io
- **Language**: TypeScript
- **Database**: PostgreSQL (typical for Backstage)
- **Authentication**: OAuth/OIDC integration
- **Documentation**: Built-in Backstage TechDocs

### 📦 PROJECT STRUCTURE
- Following Backstage monorepo structure
- Plugins-based architecture
- Microservices-oriented backend
- React-based frontend components

## Coding Standards & Conventions

### 💻 CODE STYLE
- TypeScript strict mode enabled
- ESLint + Prettier for code formatting
- Consistent naming conventions
- API-first design principles

### 🔍 QUALITY GATES
- Type safety as priority
- Clean code principles
- Proper error handling
- Unit testing coverage

## Domain Knowledge

### 🎯 PROJECT CONTEXT
- **Purpose**: Hackathon Agent Backend
- **Target**: Developer Portal using Backstage.io
- **Environment**: Cloud-native deployment ready

### 📋 BUSINESS REQUIREMENTS
- Agent-based functionality
- Integration with Backstage ecosystem
- Scalable architecture
- Modern developer experience

## Recurring Patterns

### 🔄 DEVELOPMENT PATTERNS
- Plugin-based architecture (Backstage pattern)
- Clean separation of concerns
- Configuration-driven setup
- Modular component design

## API Contracts

### 🌐 API DESIGN
- RESTful APIs following OpenAPI spec
- Authentication middleware
- Error handling standards
- Response format consistency

## Technical Learnings

### 🧠 INITIAL INSIGHTS
- Backstage.io requires specific project structure
- TypeScript configuration is crucial
- Plugin architecture provides flexibility
- Clean architecture enhances maintainability

### 📚 BACKSTAGE SPECIFICS
- Uses Lerna for monorepo management
- Requires app-config.yaml for configuration
- Plugin system for extensibility
- TechDocs for documentation
