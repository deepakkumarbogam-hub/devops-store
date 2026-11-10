# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS build

WORKDIR /app

COPY pom.xml .

RUN mvn dependency:go-offline

COPY src ./src

RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jre

WORKDIR /app

COPY --from=build --chown=10001:10001 /app/target/*.jar app.jar

USER 10001:10001

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]